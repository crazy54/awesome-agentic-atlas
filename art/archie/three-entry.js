// The slice of three.js the masthead's Archie needs, bundled into `docs/assets/three-archie.js`.
//
// Vendored instead of fetched from a CDN, so the page takes on no third-party host and no version drift. It
// is bundled from this list, not copied whole, so only what is named here ships: about 620 KB minified and
// 160 KB gzipped, against 1.4 MB for three's core alone. To rebuild, pinning the version on purpose:
//
//   npm i three@0.186.0 esbuild
//   npx esbuild art/archie/three-entry.js --bundle --minify --format=esm --legal-comments=eof \
//     --outfile=docs/assets/three-archie.js
//
// If `docs/assets/archie.js` starts using another three.js export, add it here and rebuild.
export {
  WebGLRenderer, Scene, PerspectiveCamera, DirectionalLight, AnimationMixer, LoopOnce, LoopRepeat,
  PMREMGenerator, SRGBColorSpace, NoToneMapping, Color, Vector3, Group, Mesh, SpotLight, ShaderMaterial,
  CylinderGeometry, CustomBlending, OneFactor, ZeroFactor, SrcAlphaFactor,
  OneMinusSrcAlphaFactor, DoubleSide, MeshStandardMaterial, MeshBasicMaterial, BoxGeometry, CircleGeometry,
  PlaneGeometry, WebGLRenderTarget, CanvasTexture, LinearFilter,
} from "three";
export { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
export { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
