from psd_tools import PSDImage

def inspect_psd(psd_path):
    psd = PSDImage.open(psd_path)
    
    print("=== PSD Attributes ===")
    for attr in dir(psd):
        if not attr.startswith('_'):  # Skip private attributes
            try:
                value = getattr(psd, attr)
                if not callable(value):  # Skip methods
                    print(f"{attr}: {value}")
            except Exception as e:
                print(f"{attr}: Error accessing ({e})")
    
    print("\n=== Image Resources ===")
    if hasattr(psd, 'image_resources'):
        resources = psd.image_resources
        print("Resource attributes:")
        for attr in dir(resources):
            if not attr.startswith('_'):
                try:
                    value = getattr(resources, attr)
                    print(f"{attr}: {value}")
                except Exception as e:
                    print(f"{attr}: Error accessing ({e})")
    else:
        print("No image_resources attribute found")

# Test the function
psd_path = 'your_file.psd'
inspect_psd(psd_path)
