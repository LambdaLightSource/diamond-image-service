
# Demonstrating Functionality

The Diamond Image Service supports several functionalities, accessible through structured URLs. The following is a subset of the many features the service provides:

## Upload an Image with Lifespan
Here's an example of how to set an image's lifespan during an upload:
```bash
curl -X PUT -F "media=@dahlia-8546849_1280.jpg" "http://image-service.diamond.ac.uk/unsafe/upload?lifespan=<number of days>"
```

## Resizing
Resize an image to 300x200 pixels:
```bash
https://image-service.diamond.ac.uk/unsafe/300x200/filename.jpg
```

## Changing Image Formats
Convert an image to PNG:
```bash
https://image-service.diamond.ac.uk/unsafe/300x200/filename.jpg.png
```

## Cropping Images
Crop an image to focus on a specific area:
```bash
https://image-service.diamond.ac.uk/unsafe/100x100:200x200/filename.jpg
```

## Rotating Images
Rotate an image by 90 degrees:
```bash
https://image-service.diamond.ac.uk/unsafe/filters:rotate(90)/filename.jpg
```

## Applying Filters
Apply a grayscale filter:
```bash
https://image-service.diamond.ac.uk/unsafe/filters:grayscale()/filename.jpg 
```