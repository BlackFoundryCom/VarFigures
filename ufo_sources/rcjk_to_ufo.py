"""
Script to convert figArnaud.rcjk to UFO with Variable Components, according
to the https://github.com/BlackFoundryCom/variable-components-in-ufo/ proposal.

It is not a general .rcjk to .ufo conversion script (yet), as it requires some
manual set up.

This uses Fontra backends to do the heavy lifting.
"""

import asyncio
import pathlib
import ufoLib2
from fontra.backends.designspace import DesignspaceBackend
from fontra_rcjk.backend_fs import RCJKBackend


repoRoot = pathlib.Path(__file__).resolve().parent.parent
rcjkSource = repoRoot/ "figArnaud.rcjk"
ufoSourceDir = repoRoot / "ufo_sources"
dsPath = ufoSourceDir / "figArnaud.designspace"
ufoPath = ufoSourceDir / "figArnaud.ufo"


def renameLayer(layerName):
    # Hack
    assert layerName[:8] == "regular/"
    return layerName[8:]


async def main():
    rcjkFont = RCJKBackend.fromPath(rcjkSource)
    ufoFont = ufoLib2.Font.open(ufoPath)

    revCmap = await rcjkFont.getReverseCmap()
    glyphs = {}
    for glyphName in revCmap:
        glyphs[glyphName] = glyph = await rcjkFont.getGlyph(glyphName)
        for fontraLayer in glyph.layers:
            # Set up UFO layers since Fontra can't yet
            layerName = fontraLayer.name
            if layerName not in ufoFont.layers:
                ufoFont.newLayer(layerName)
    ufoFont.save()

    dsFont = DesignspaceBackend.fromPath(dsPath)
    # Fiddle with internal mappings as Fontra can't figure out the right layer names yet
    dsFont.ufoGlyphSets = {renameLayer(k): v for k, v in dsFont.ufoGlyphSets.items()}
    dsFont.fontraLayerNames = {
        k: renameLayer(v) for k, v in dsFont.fontraLayerNames.items()
    }
    dsFont.ufoLayers = {renameLayer(k): v for k, v in dsFont.ufoLayers.items()}

    for glyphName, glyph in glyphs.items():
        await dsFont.putGlyph(glyphName, glyph)


asyncio.run(main())
