import * as THREE from "https://cdn.skypack.dev/three@0.132.2";
import {GLTFLoader} from "https://cdn.skypack.dev/three@0.132.2/examples/jsm/loaders/GLTFLoader.js";
import {OrbitControls} from "https://cdn.skypack.dev/three@0.132.2/examples/jsm/controls/OrbitControls.js";


class LoadModelScene {
    constructor() {
        this._Initialize();
    }

    _Initialize() {
        this._scene = new THREE.Scene();
        this._camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this._camera.position.setZ(10);
        this._renderer = new THREE.WebGLRenderer({
            canvas: document.getElementsByClassName("webgl")[0]
        });
        
        this._renderer.setPixelRatio(window.devicePixelRatio);
        this._renderer.setSize( window.innerWidth, window.innerHeight);
        this._renderer.render(this._scene, this._camera);
        this._renderer.shadowMap.enabled = true;
        this._renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.body.appendChild( this._renderer.domElement );
        
            
        this._controls = new OrbitControls(this._camera, this._renderer.domElement);
        this._LoadGLTFModel();
        this._RAF();
        this._InitializeLights();
        this._InitializePlane();
        this._CameraPath();
    }

    _InitializePlane() {
        const plane = new THREE.Mesh(
            new THREE.PlaneGeometry(100, 100, 10, 10),
            new THREE.MeshStandardMaterial({
                color: 0x202020,
            }));
            plane.castShadow = false;
            plane.receiveShadow = true;
            plane.rotateX(Math.PI/2);
            this._scene.add(plane);
            
            window.addEventListener('resize', () => {
                this._OnWindowResize();
            }, false);
    }
    
    _CameraPath() {
        // Define a path for the camera to follow
        this.numKeyframes = 2500;
        this.keyframes = [];
        this.keyframesTarget = [];
        this.frameIndex = 0;
        
        const curve = new THREE.CubicBezierCurve3(
            new THREE.Vector3(7, 7, 5),
            new THREE.Vector3(-25, 2, 25),
            new THREE.Vector3(9, 0.5, -27.5),
            new THREE.Vector3(7, 7, 5)
        );
        const curveTarget = new THREE.CubicBezierCurve3(
            new THREE.Vector3(-5, 3, 0),
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(5, 0, 0),
            new THREE.Vector3(-5, 3, 0)
        );
        
        for (let i = 0; i < this.numKeyframes; i++) {
            const point1 = curve.getPoint(i / this.numKeyframes);
            const point2 = curveTarget.getPoint(i / this.numKeyframes);
            this.keyframes.push(point1);
            this.keyframesTarget.push(point2);
            
        }
    }

    _InitializeLights   () {
        // let light = new THREE.DirectionalLight(0xFFFFFF, 1);
        // light.position.set(0, 2, 0);
        // light.target.position.set(0, 0, 0);
        // light.castShadow = true;
        // light.shadow.mapSize.width = 128;
        // light.shadow.mapSize.height = 128;

        // this._scene.add(light);
        // this._scene.add(light.target);

        let pointLight = new THREE.PointLight(0xFFFFFF, 1);
        pointLight.position.set(-3, 5, 5);
        pointLight.castShadow = true;
        this._scene.add(pointLight);
        let pointLightHelper1 = new THREE.PointLightHelper(pointLight);
        this._scene.add(pointLightHelper1);
        
        // let pointLight2 = new THREE.PointLight(0x3377ff, 2);
        // pointLight2.position.set(2,2,3);
        // pointLight2.castShadow = true;
        // this._scene.add(pointLight2)
        // let pointLightHelper2 = new THREE.PointLightHelper(pointLight2);
        // this._scene.add(pointLightHelper2);
        
        // let ambientLight = new THREE.AmbientLight(0xffffff, 2);
        // ambientLight.castShadow = true;
        // this._scene.add(ambientLight);

        
        let directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.castShadow = true;
        directionalLight.position.set(0,7,4);
        this._scene.add(directionalLight);
        
        // let directionalLightHelper1 = new THREE.DirectionalLightHelper(directionalLight);
        // this._scene.add(directionalLightHelper1);
        

        // let gridHelper = new THREE.GridHelper();
        // this._scene.add(gridHelper);
        this._scene.background = new THREE.Color('#111111');
        // this._scene.background = new THREE.Color('#565555');
        
    }

    _LoadGLTFModel() {
        const loader = new GLTFLoader();
        loader.load("/static/worldmap/IonTrapApplicationFacility.glb", (gltf) => {
            gltf.scene.scale.multiplyScalar(10);
            gltf.scene.rotateX(-Math.PI/2)
            this._scene.add(gltf.scene);
            console.log("GLTF loaded.");
        });
    }

    _OnWindowResize() {
        this._camera.aspect = window.innerWidth / window.innerHeight;
        this._camera.updateProjectionMatrix();
        this._renderer.setSize(window.innerWidth, window.innerHeight);
    }

    _RAF() {
        requestAnimationFrame(() => {
            this._RAF();
            //this._controls.update()
            this._camera.position.copy(this.keyframes[this.frameIndex]);
            this._camera.lookAt(this.keyframesTarget[this.frameIndex]);
            this.frameIndex = (this.frameIndex + 1) % this.numKeyframes;
            this._renderer.render(this._scene, this._camera);
            /*
            document.getElementById('info').innerHTML = `Camera Position: (${camera.position.x.toFixed(2)}, ${camera.position.y.toFixed(2)}, ${camera.position.z.toFixed(2)})<br>Camera Target: (${controls.target.x.toFixed(2)}, ${controls.target.y.toFixed(2)}, ${controls.target.z.toFixed(2)})`;
            console.log("Camera Position:", {
                x: camera.position.x.toFixed(0),
                y: camera.position.y.toFixed(0),
                z: camera.position.z.toFixed(0)
            });
            */
        });
    }
}

let _APP = null;

window.addEventListener('DOMContentLoaded', () => {
  _APP = new LoadModelScene();
});