#!/usr/bin python3
import os
import argparse
import pandas as pd

import plaython as pt
import plaython.backstage as pbs
import numpy as np
import warnings

from plaython.models import PersonaMapperScorer, pm_gpt_scorer
from plaython.log import build_logger
from plaython.db import get_redis_client, RedisManager

warnings.filterwarnings('ignore', category=UserWarning)
parser = argparse.ArgumentParser(description="CoupangPlay PVR Trainer")
# Testing options
parser.add_argument("--debug", action="store_true", default=False)
parser.add_argument("--local", action="store_true", default=False)
parser.add_argument("--dev", action="store_true", default=False)

# External configuration
parser.add_argument("--abtest", nargs="?", default=False, const=True)
parser.add_argument("--feed", type=str, default="ALL")
parser.add_argument("--mute", action="store_true", default=False)
parser.add_argument("--skip-gg", action="store_true", default=False)
parser.add_argument("--manual-boost", type=int, default=2)

# Redis configuration
parser.add_argument("--redis-host", type=str,
                    default="clustercfg.discover2-prod-cluster.1uxtgm.apn2.cache.amazonaws.com")
parser.add_argument("--redis-port", type=int, default=6379)

args = vars(parser.parse_args())

if __name__ == "__main__":
    logger = build_logger(mute=args["mute"])

    # Hard include for internal testing
    add_if_possible = {
        "c2b54b86-e199-46c2-8e43-7f7d3692ecff",  # Mia
        "52663619-24a2-47a5-991b-5c1bd0cf9120",  # Chris
        "5227b0e4-5474-4a15-8065-75a997b908ef",  # Dana
        "ed4c6140-4118-4352-b12e-f5be18ebd445",  # Alex
        "42daf423-a795-4a7d-bec0-ad13bc189eb2",  # Sean
        "7b592bd8-1916-4f41-8caf-689fe65aefb4",  # Celina
        "ea0f6e97-64ca-4df1-b520-e31da9bccf54",  # Judy
    }

    # Redis
    envs = os.environ
    rc = get_redis_client(redis_host=args["redis_host"],
                          redis_port=args["redis_port"],
                          redis_password=envs["REDIS_PASSWORD"])
    rm = RedisManager(rc, logger=logger)

    # Data Ingestion
    files = pt.list_customer()
    df = pt.read_s3(files, columns=["profile_id", "profile_type", "title_engagement"],
                    filter_=pt.watch_ratio_filter)
    add_if_possible = {i for i in add_if_possible if i in df["profile_id"].values}

    video = pt.read_video(exclude_expired=True)
    video = video[video["content_type"].isin({"TVSHOW", "MOVIE"})]

    # Feed click data
    feed_nav = pt.read_s3(pt.list_files("s3://p-window-ml-prod/data/feed_navigation/click/aggr/dt={date}"))
    feed_nav = feed_nav.set_index("profile_id")
    feed_nav.columns = feed_nav.columns.str.upper()
    feed_nav = feed_nav[["ALL", "TVSHOWS", "MOVIES", "TVOD"]]

    # collections
    cm = pbs.CollectionManager(video, logger)
    auto = pd.read_json("s3://p-window-ml-prod/data/mlco/latest.json", lines=True)
    # temporal replacement; need a permanent fix from automated collection generation
    auto["feed"] = auto["feed"].replace({"MOVIE": "MOVIES", "TVSHOW": "TVSHOWS"})
    for feed in ("ALL", "TVSHOWS", "MOVIES", "TVOD"):
        if (feed != "ALL") and (args["abtest"] != "B"):
            continue
        coll = cm.get_collections(category=feed, use_static=True, use_prefix=True)

        auto_feed = auto[auto["feed"].eq(feed)]

        # Remove START
        # this part once old collections are removed from CMS
        replaced = []
        for i, row in coll.iterrows():
            m = auto_feed["row_names"].eq(row["row_names"])
            if m.any() and (m.sum() == 1):
                j, titles = next(auto_feed[m]["titles"].items())
                coll.at[i, "titles"] = titles
                replaced.append(j)
        auto_feed = auto_feed[~auto_feed.index.isin(replaced)]
        # Remove END

        coll = cm.add_collections(coll,
                                  auto_feed["row_names"], auto_feed["titles"],
                                  types="mlco")
        coll = cm.check_pinned(coll)
        cm.set_info(coll, category=feed)
        _, xpin = cm.preprocess(coll, filter_expiry=0, category=feed)

        # scorers
        pms = PersonaMapperScorer(video)
        pms.fit(xpin["titles"])
        gpt = pm_gpt_scorer(xpin["titles"])

        info = cm.get_info(category=feed)

        free_size = info["free_size"] = info["target_size"] - info["personalized_size"]
        mlco_final_size = min([info["mlco_size"], info["personalized_size"]])

        on_feed = xpin.query("on_feed").index.tolist()
        mlco_feed = xpin[xpin["types"].eq("mlco")].index.tolist()
        mlco_final_size = min(mlco_final_size, len(mlco_feed))

        rest_feed = xpin[xpin["types"].ne("mlco") & ~xpin["on_feed"]].index.tolist()
        pers_final_size = info["personalized_size"] - mlco_final_size

        indices = {
            "on_feed": (on_feed, free_size),
            "mlco_feed": (mlco_feed, mlco_final_size),
            "pers_feed": (rest_feed, pers_final_size)
        }

        candidate_vids = dict(xpin["titles"].items())
        candidate_names = dict(xpin["row_names"].items())

        assert sum(len(i) for _, (i, _) in indices.items()) == xpin.shape[0]

        if xpin.shape[0] <= 256:
            dtype = np.uint8
        else:
            dtype = np.uint16

        pids = []
        res = []

        if feed == "ALL":
            feed_df = df
        else:
            target_ids = set(feed_nav.index[feed_nav[feed].gt(0)]) | add_if_possible
            feed_df = df[df["profile_id"].isin(target_ids)]

        for _, d in feed_df[["profile_id", "video_ids"]].groupby(np.arange(feed_df.shape[0]) // 2048):
            pm_score = pms.predict(d["video_ids"])
            pm_score = pm_score.div(pm_score.sum(axis=1).clip(1e-5), axis=0)
            gpt_raw_score, gpt_coll_score = gpt(d["video_ids"])
            final_score = (pm_score * 2 + gpt_coll_score) / 3

            ps, vs = [], []

            for t, (ind, k) in indices.items():
                a = final_score[ind]
                if t == "on_feed":
                    # manual curation booster
                    a *= args["manual_boost"]
                tmp = np.argpartition(a, -k, axis=1)[:, -k:]
                ps.append(a.columns.values[tmp])
                vs.append(np.partition(a, -k, axis=1)[:, -k:])

            ps = np.hstack(ps)
            vs = np.hstack(vs)

            selected = np.take_along_axis(ps, np.argsort(vs, axis=1)[:, ::-1], axis=1).astype(dtype)
            pids.append(d["profile_id"].values)
            res.append(selected)

        pids = np.hstack(pids)
        res = np.vstack(res)

        it = cm.prepare_output(pids, res, category=feed, abtest=args["abtest"])
        rm.publish(it, abtest=args["abtest"], field="pm:" + feed)
