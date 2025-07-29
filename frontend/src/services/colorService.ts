export function rgbToHsl([r, g, b]: [number, number, number]): [number, number, number] {
    r /= 255;
    g /= 255;
    b /= 255;

    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h: number = 0, s: number, l: number = (max + min) / 2;

    if (max === min) {
        h = s = 0; // achromatic
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return [h, s, l];
}

export function hslToRgb([h, s, l]: [number, number, number]): [number, number, number] {
    let r: number, g: number, b: number;

    if (s === 0) {
        r = g = b = l; // achromatic
    } else {
        const hue2rgb = (p: number, q: number, t: number): number => {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1 / 6) return p + (q - p) * 6 * t;
            if (t < 1 / 2) return q;
            if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        }

        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        r = hue2rgb(p, q, h + 1 / 3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3);
    }

    return [r * 255, g * 255, b * 255].map(v => Math.round(v)) as [number, number, number];
}

export function boostLightness(rgb: [number, number, number], lightenFactor = 0.2): [number, number, number] {
    let [h, s, l] = rgbToHsl(rgb);
    l = Math.min(1, l + lightenFactor); // increase lightness
    return hslToRgb([h, s, l]);
}

export function rgbToHex(rgb: [number, number, number]): string {
    return `#${rgb.map(c => c.toString(16).padStart(2, "0")).join("")}`;
}
