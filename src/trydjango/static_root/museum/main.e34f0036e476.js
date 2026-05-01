import * as THREE from "https://cdn.skypack.dev/three@0.132.2";
import {OrbitControls} from "https://cdn.skypack.dev/three@0.132.2/examples/jsm/controls/OrbitControls.js";



const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer({antialias: true, canvas: document.querySelector("#c")}); 
const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 1, 1000);
const controls = new OrbitControls(camera, renderer.domElement);
controls.keys = {
	LEFT: 'ArrowLeft', //left arrow
	UP: 'ArrowUp', // up arrow
	RIGHT: 'ArrowRight', // right arrow
	BOTTOM: 'ArrowDown' // down arrow
}
camera.position.set( 0, 20, 20 );
controls.update();

renderer.setSize(window.innerWidth, window.innerHeight);   



const productData = await fetch('/api/artworks/').then(r => r.json());




class Plane {
    
    static textureLoader = new THREE.TextureLoader();
    
    constructor(data, pos) {
        this.data = data;
        this.plane = null;
        this.pos =  (Math.PI/6)*pos;
    }

    async _CreatePlane(scene) {
        const boxWidth = 30;
        const boxHeight = 15;
        const boxDepth = 0.1;
        const geometry = new THREE.BoxGeometry(boxWidth, boxHeight, boxDepth);
        const material = new THREE.MeshBasicMaterial({color: 0xffffff });
        this.plane = new THREE.Mesh(geometry, material);
        this.plane.position.x = Math.sin(this.pos)*50;
        this.plane.position.y = this.pos*3;
        this.plane.position.z = Math.cos(this.pos)*50;
        console.log(this.plane.position);
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

const planes = [];

for (const [index, data] of productData.entries()) {
    const plane = new Plane(data, index);
    await plane._CreatePlane(scene);
    await plane._LoadTexture();
    planes.push(plane);
}


function RAF(time) {
    time = time * 0.0001;
    controls.update();
    renderer.render(scene, camera);
    scene.traverse(object => {
        if (object.isMesh) {
            object.rotation.y = time;
        }
    });
        
    requestAnimationFrame(RAF);   
}

RAF();

