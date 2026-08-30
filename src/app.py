import os
import shutil
import gradio as gr
import numpy as np
import plotly.graph_objects as go
import cache
import embed
import reduce

UPLOADS = os.path.join(cache.ROOT, "uploads")

def extract_inputs(files, folder_files, text_paths):
    dirs = [p.strip() for p in (text_paths or "").splitlines() if p.strip()]

    if files:
        dest = os.path.join(UPLOADS, "images")
        os.makedirs(dest, exist_ok=True)
        for f in files:
            p = f if isinstance(f, str) else getattr(f, "name", str(f))
            if os.path.isfile(p):
                shutil.copy(p, os.path.join(dest, os.path.basename(p)))
        if dest not in dirs:
            dirs.append(dest)

    if folder_files:
        for f in folder_files:
            p = f if isinstance(f, str) else getattr(f, "name", str(f))
            orig = getattr(f, "orig_name", "") or os.path.basename(p)
            folder_name = orig.split("/")[0] if "/" in orig else "uploaded_folder"
            dest = os.path.join(UPLOADS, folder_name)
            os.makedirs(dest, exist_ok=True)
            if os.path.isfile(p):
                shutil.copy(p, os.path.join(dest, os.path.basename(orig or p)))
            if dest not in dirs:
                dirs.append(dest)

    return list(dict.fromkeys(dirs))


def process(files, folder_files, text_paths, method, force):
    folders = extract_inputs(files, folder_files, text_paths)
    if not folders:
        raise gr.Error("upload images/folder or a folder path")

    embedder, all_embeds, all_paths, all_labels = None, [], [], []

    for folder in folders:
        if not os.path.isdir(folder):
            continue
        label = os.path.basename(folder.rstrip("/"))
        cached = None if force else cache.load(folder)

        if cached is None:
            if embedder is None:
                embedder = embed.Embedder()
            cached = embedder.folder(folder)
            cache.save(folder, cached)

        for fname, vec in cached.items():
            all_embeds.append(vec)
            all_paths.append(os.path.join(folder, fname))
            all_labels.append(label)

    if not all_embeds:
        raise gr.Error("no images found in inputs")

    if len(all_embeds) < 15 and method in ["umap", "tsne"]:
        raise gr.Error(f"upload at least 15 images or choose PCA.")

    points = reduce.reduce(np.stack(all_embeds), method)
    fig = go.Figure()
    for label in dict.fromkeys(all_labels):
        idx = [i for i, l in enumerate(all_labels) if l == label]
        fig.add_trace(go.Scatter(
            x=points[idx, 0], y=points[idx, 1],
            mode="markers", name=label,
            text=[all_paths[i] for i in idx],
            hovertemplate="%{text}<extra></extra>",
            marker=dict(size=6, opacity=0.8),
        ))
    fig.update_layout(template="plotly_dark", title="embedding space", margin=dict(l=20, r=20, t=40, b=20))
    return fig


with gr.Blocks(title="space") as app:
    gr.Markdown("# space\n embeddings")

    with gr.Row():
        with gr.Column(scale=2):
            with gr.Row():
                upload_files = gr.File(label="upload images", file_count="multiple")
                upload_folder = gr.File(label="upload folder", file_count="directory")
            paths = gr.Textbox(label="or local folder paths (optional)", placeholder="/path/to/folder (one per line)", lines=2)
        with gr.Column(scale=1):
            method = gr.Dropdown(["umap", "tsne", "pca"], value="umap", label="method")
            gr.Markdown("UMAP/t-SNE needs atleast 15 images.")
            force = gr.Checkbox(label="recompute")
            btn = gr.Button("generate", variant="primary")

    plot = gr.Plot(label="embeddings")
    btn.click(process, [upload_files, upload_folder, paths, method, force], plot)

if __name__ == "__main__":
    app.launch(allowed_paths=[cache.ROOT])
