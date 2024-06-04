# Parse base options
options = BaseOptions()
opts = options.parse()

# Select mode and corresponding YAML input or model path
yaml_input = f"yolov10_{opts.model_size}.yaml"
model_input = yaml_input if (opts.mode == "train" and not opts.resume) else opts.model_path
model = YOLO(model_input)

# Initialize model based on selected mode
print(f"Selected Mode: {opts.mode}")
print("Model Setting Completed. Start the mode.\n")

# Execute operation based on mode
if opts.mode == "train":
    model.train(data=opts.train_dataset, epochs=opts.epochs)
elif opts.mode == "validation":
    metrics = model.val()
elif opts.mode == "test":
    results = model(opts.video_path)
elif opts.mode == "track":
    model.track(opts.video_path)
