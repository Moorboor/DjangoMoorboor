import * as THREE from "https://cdn.skypack.dev/three@0.132.2";
import {TrackballControls} from 'https://cdn.skypack.dev/three@0.132.2/examples/jsm/controls/TrackballControls.js';
// import {OrbitControls} from "https://cdn.skypack.dev/three@0.132.2/examples/jsm/controls/OrbitControls.js";

class Plane {
    
    static textureLoader = new THREE.TextureLoader();
    
    constructor(data, width=2, height=1) {
        this.width = width;
        this.height = height;
        this.data = data;
        this.plane = null;
    }

    async _CreatePlane(scene) {
        const boxWidth = 1;
        const boxHeight = 1;
        const boxDepth = 1;
        const geometry = new THREE.BoxGeometry(boxWidth, boxHeight, boxDepth);
        const material = new THREE.MeshBasicMaterial({color: 0xffffff });
        this.plane = new THREE.Mesh(geometry, material);
        scene.add(this.plane);
        return scene;
    }
    
    async _LoadTexture() {
        Plane.textureLoader.load(this.data.image_url, (texture) => {
            this.plane.material.map = texture;
            this.plane.material.needsUpdate = true;
        });
    }
}

class SceneManager {

    constructor() {
        this.sceneInfos = [];
        this.productData = null;
        this.renderer = new THREE.WebGLRenderer({antialias: true, canvas: document.querySelector("#c"), alpha : true}); 
        this.renderer.setSize(window.innerWidth, window.innerHeight);   
        this.renderer.setScissorTest(true);
        this._FetchProductData().then(async () => { // Wrap the callback in an async function
                await this._CreateHTMLGrid();
                await this._CreatePlanes();
                requestAnimationFrame(this._Animate);
            });
    }

    async _FetchProductData(){
        const response = await fetch(`/api/artworks/`);
        this.productData = await response.json();
    }

    async _MakeScene(elem) {
        const scene = new THREE.Scene();
        // scene.background = new THREE.Color('red');
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 1, 1000);

        const controls = new TrackballControls(camera, elem);
        controls.noZoom = true;
        controls.noPan = true;
        scene.add(camera);
        camera.position.set(0, 0, 2.2);
        // {
		// 	const color = 0xFFFFFF;
		// 	const intensity = 3;
		// 	const light = new THREE.DirectionalLight( color, intensity );
		// 	light.position.set( - 1, 2, 4 );
		// 	camera.add(light);
        // }
        return { scene, camera, controls, elem };
    }

    async _CreatePlanes() {
        for (const [index, data] of this.productData.entries()) {
            const canvasEl = document.getElementById(`scene-${index + 1}`);
            if (!canvasEl) continue;
            
            const { scene, camera, controls, elem } = await this._MakeScene(canvasEl);
            const plane = new Plane(data);
            await plane._CreatePlane(scene);
            await plane._LoadTexture();
            this.sceneInfos.push({ scene, camera, controls, elem });
        }
    }

    _CreateHTMLGrid() {

        const grid = document.querySelector(".grid"); 
        this.productData.forEach((data, index) => {
            const card = document.createElement("div");
            card.className = "card";
            card.dataset.title = data.title;
            card.dataset.desc = data.description;

            const canvas = document.createElement("canvas");
            canvas.id = `scene-${index + 1}`;
            canvas.style.width = "100%";
            canvas.style.height = "180px";
            canvas.style.display = "block";

            const body = document.createElement("div");
            body.className = "body";
            const h3 = document.createElement("h3");
            h3.textContent = data.title;
            const p = document.createElement("p");
            p.textContent = data.description;

            body.appendChild(h3);
            body.appendChild(p);

            card.appendChild(canvas);
            card.appendChild(body);
            grid.appendChild(card);

        });
    }

    async _RenderSceneInfo() {
        for (const sceneInfo of this.sceneInfos) {
            const {scene, camera, elem} = sceneInfo;
            const {left, right, top, bottom, width, height} = elem.getBoundingClientRect();
            
            const isOffscreen = bottom < 0 || top > this.renderer.domElement.clientHeight || right < 0 || left > this.renderer.domElement.clientWidth;
            if (isOffscreen) {
                continue;
            }
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            const positiveYUpBottom = this.renderer.domElement.clientHeight - bottom;
            this.renderer.setScissor(left, positiveYUpBottom, width, height);
            this.renderer.setViewport(left, positiveYUpBottom, width, height);
            this.renderer.render(scene, camera);
        }
    }
    
    async _ResizeRendererToDisplaySize() {
        const canvas = this.renderer.domElement;
        const pixelRatio = window.devicePixelRatio; //  Handling HD-DPI displays
        const width  = Math.floor( canvas.clientWidth  * pixelRatio );
        const height = Math.floor( canvas.clientHeight * pixelRatio );
        const needResize = canvas.width !== width || canvas.height !== height;
        if (needResize) {
            this.renderer.setSize(width, height, false);
        }
        return needResize;
    }

    _Animate = (time) => {
        time *= 0.00012; 
        this._RenderSceneInfo();
        
        for (const sceneInfo of this.sceneInfos) {
            const {scene, camera, controls, elem} = sceneInfo;
            scene.traverse(object => {
                if (object.isMesh) {
                    object.rotation.y = time;
                }
            });
            controls.handleResize();
            controls.update();  
        }
        requestAnimationFrame(this._Animate);    
    }
    
}
        

const sceneManager = new SceneManager();