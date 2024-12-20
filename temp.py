Here's the English translation:

Introduction
I have reviewed unfinished tasks from this year and thought about additional features that need to be developed, such as poster-related work, along with other potential initiatives. Since a new team member is expected to join in February, I've expanded my thinking to include tasks for them to work on, which has resulted in more items than initially planned. While some tasks may not be high priority, I've considered projects that could be interesting from a long-term perspective.

1. Episodes
Episode detection is the first priority. We've spent considerable time developing the model, and now that the pipeline development is complete, we're in the performance evaluation phase. Once we finish performance evaluation and confirm quality standards, the next step will be batch processing for production implementation. While this won't take long, it requires effort from the Backend side to integrate with CMS, and since a developer hasn't been assigned yet, discussion with the PO will be necessary. We're also considering publishing a blog post about the results and filing patents to secure intellectual property rights. Poster-related work is divided into three main areas: improving output image quality, reducing poster generation processing time, and exploring better images.

2. Regarding image quality, we received feedback about poster image trends from the CD team, indicating that images need to be brighter and clearer. We plan to address this quickly in a short period. We can either use statistical measures or libraries like cv2 to increase overall brightness and enhance clarity. We'll also consider advanced methods for creating better images.

3. Next, poster generation currently takes at least 20 minutes per episode, causing significant user inconvenience and potential instance usage cost issues. Therefore, optimizing speed from both CD member UX and cost perspectives is crucial.

4. Another aspect is improving image selection quality. The first goal is to create a regression model for rating image attractiveness. Currently, we show about 60 images (10 images each for 3 characters in both vertical and horizontal types). Since many images don't require evaluation, we aim to show only the better images to reduce designers' time and help make more rational decisions.

5. Next is the auto-matching component of the PTSD project initiated by Tyler. Currently, the ingestion bucket and CMS titles aren't connected in real-time. Development is needed to enable immediate CMS integration based on file triggers in the ingestion bucket. This requires building CMS site functionality for uploading content and meta information during onboarding. While important, this needs more discussion, especially since Tyler's departure. This integration would benefit ML tasks by providing episode information for detection, eliminating the need to parse filenames for episode numbers, and providing necessary transcoding information.

6. Regarding video QC, besides episode detection, we've received various requirements. Some features like Aspect Ratio estimation for detecting pillarbox/letterbox are already developed, while others like voice-lip sync need development. These tasks should be prioritized and listed for development in 2025 according to PO items. I believe we can completely save the 30 minutes per episode currently spent on QC when we can fully replace these QC tasks.

7. Next is transcoding parameter optimization. This task aims to find optimal transcoding/encoding parameters considering cost and video quality. It's Joy's project, and I heard a new streaming team expert has joined. We can proceed with discussions about POC content with Joy. The ultimate goal is to extract temporal-aware embeddings from videos, measure shot similarity through these embeddings, and develop methodologies for parameter optimization.

8. For 2024, one of Steve's items with significant business impact is automatic sports highlight generation. While our company heavily features sports broadcasting, the lack of ML functionality in this area is a concern. Creating a feature for sports highlight generation this year could have substantial business impact.

9. Lastly, while lower in priority, I've considered this as an Open Problem. With recent developments like OpenAI's Sora and Google's VEO2 in video generation models, and as a video content company, we should consider the potential value of this technology. We could potentially generate attractive preview screens for hero or rail titles, or use them for marketing on YouTube and other channels. If possible, we could try open-source models or develop in-house technology with fine-tuning as a long-term project. This could be an interesting initiative.

I've shared these nine proposed items, and that concludes my presentation.
