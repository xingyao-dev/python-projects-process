# Animation assets

The current build uses procedural portraits with Live2D-style idle motion:
breathing, sway, blinking and collar shine.

Actual Live2D Cubism / Spine / DragonBones playback requires:

- licensed model exports (`.moc3`, `.skel` / `.atlas`, DragonBones JSON),
- the corresponding runtime or SDK,
- license compliance for both the character art and the runtime.

This repository does not bundle proprietary SDKs or downloaded character art.
Drop licensed PNG portraits into `assets/portraits/` for image-based portraits.
