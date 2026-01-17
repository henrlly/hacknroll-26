export function getVideoDuration(videoUrl: string): Promise<number> {
  return new Promise((resolve, reject) => {
    // Use the Audio constructor as a minimal media element instance
    // A hidden video element (document.createElement('video')) also works
    const media = new Audio();

    // Event listener to fire when media metadata is loaded
    media.onloadedmetadata = () => {
      resolve(media.duration);
      // Clean up the object URL if a Blob or File was used
      if (videoUrl.startsWith('blob:')) {
        URL.revokeObjectURL(videoUrl);
      }
    };

    // Error handler
    media.onerror = () => {
      reject(new Error('Failed to load video metadata.'));
      // Clean up in case of error
      if (videoUrl.startsWith('blob:')) {
        URL.revokeObjectURL(videoUrl);
      }
    };

    // Set the source and preload metadata
    media.preload = 'metadata'; // Hint to load only metadata
    media.src = videoUrl;
  });
}
