"""Turns a Geofabrik .poly file into the bbox and a simplified outline the app needs (to hide the online tracks there)."""
import json
import sys


def read_poly(path):
    rings, ring, hole = [], None, False
    with open(path) as f:
        lines = [l.strip() for l in f][1:]
    for line in lines:
        if not line:
            continue
        if line == 'END':
            if ring is not None:
                if not hole:
                    rings.append(ring)
                ring = None
            continue
        if ring is None:
            hole = line.startswith('!')
            ring = []
            continue
        lon, lat = (float(v) for v in line.split()[:2])
        ring.append((lon, lat))
    return rings


def simplify(points, tol):
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        a, b = stack.pop()
        (ax, ay), (bx, by) = points[a], points[b]
        dx, dy = bx - ax, by - ay
        norm = (dx * dx + dy * dy) ** 0.5 or 1e-12
        best, at = 0.0, -1
        for i in range(a + 1, b):
            px, py = points[i]
            d = abs(dy * (px - ax) - dx * (py - ay)) / norm
            if d > best:
                best, at = d, i
        if best > tol and at != -1:
            keep[at] = True
            stack += [(a, at), (at, b)]
    return [p for p, k in zip(points, keep) if k]


def main(poly, out):
    rings = read_poly(poly)
    xs = [p[0] for r in rings for p in r]
    ys = [p[1] for r in rings for p in r]
    bbox = [round(min(xs), 4), round(min(ys), 4), round(max(xs), 4), round(max(ys), 4)]
    tol = 0.01
    while True:
        # A closed ring starts and ends at the same point, so simplify its two halves.
        outline = [simplify(r[: len(r) // 2 + 1], tol)[:-1] + simplify(r[len(r) // 2 :], tol) for r in rings]
        outline = [r for r in outline if len(r) >= 4]
        if sum(len(r) for r in outline) <= 600:
            break
        tol *= 1.5
    polygons = [[[[round(x, 4), round(y, 4)] for x, y in r]] for r in outline]
    for p in polygons:
        if p[0][0] != p[0][-1]:
            p[0].append(p[0][0])
    json.dump({'bbox': bbox, 'boundary': {'type': 'MultiPolygon', 'coordinates': polygons}}, open(out, 'w'))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
