import fs from 'node:fs';
import path from 'node:path';

export const load = async () => {
    const examplesDir = path.join(process.cwd(), 'static', 'examples');
    
    let videos: string[] = [];

    try {
        if (fs.existsSync(examplesDir)) {
            const files = fs.readdirSync(examplesDir);
            videos = files.filter(file => {
                const ext = path.extname(file).toLowerCase();
                return ['.mp4', '.webm', '.ogg', '.mov'].includes(ext);
            });
        }
    } catch (err) {
        console.error('Error reading examples directory:', err);
    }

    return {
        videos
    };
};
