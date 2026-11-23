"use client";
import { useEffect, useRef } from "react";
import * as THREE from "three";
export default function OrbitScene() {
  const host = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const target = host.current!;
    let renderer: THREE.WebGLRenderer;
    try { renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: "low-power" }); }
    catch { return; } // CSS fallback preserves the composition without WebGL.
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5)); renderer.setClearColor(0x000000, 0);
    target.appendChild(renderer.domElement); target.classList.add("webgl-ready");
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100); camera.position.set(0, 0, 9);
    scene.add(new THREE.AmbientLight(0xffd9b8, 1.3));
    const sun = new THREE.DirectionalLight(0xffe0ad, 4.5); sun.position.set(-3, 3, 4); scene.add(sun);
    const group = new THREE.Group(); group.rotation.z = -0.3; scene.add(group);
    group.add(new THREE.Mesh(new THREE.SphereGeometry(1.62, 64, 48), new THREE.MeshStandardMaterial({ color: 0xd98446, roughness: 1 })));
    const rings = new THREE.Mesh(new THREE.RingGeometry(2.15, 2.24, 160), new THREE.MeshBasicMaterial({ color: 0xf3cda1, side: THREE.DoubleSide, transparent: true, opacity: 0.72 })); rings.rotation.x = Math.PI * 0.36; group.add(rings);
    const orbit = new THREE.Mesh(new THREE.RingGeometry(2.7, 2.705, 180), new THREE.MeshBasicMaterial({ color: 0x9ebbbd, side: THREE.DoubleSide, transparent: true, opacity: 0.35 })); orbit.rotation.x = Math.PI * 0.36; group.add(orbit);
    const moon = new THREE.Mesh(new THREE.SphereGeometry(0.13, 20, 16), new THREE.MeshStandardMaterial({ color: 0xd7e0d2, roughness: 1 })); moon.position.set(2.5, 0.45, 0); scene.add(moon);
    const stars = new Float32Array(180 * 3); let seed = 12;
    for (let i = 0; i < stars.length; i++) { seed = (seed * 16807) % 2147483647; stars[i] = (seed / 2147483647 - 0.5) * (i % 3 === 2 ? 4 : 14); }
    const geometry = new THREE.BufferGeometry(); geometry.setAttribute("position", new THREE.BufferAttribute(stars, 3));
    scene.add(new THREE.Points(geometry, new THREE.PointsMaterial({ color: 0xdfe9e2, size: 0.018, transparent: true, opacity: 0.8 })));
    const reduce = matchMedia("(prefers-reduced-motion: reduce)"); let frame = 0; let visible = true; let previous = 0;
    function draw(time = 0) {
      const delta = previous ? Math.min((time - previous) / 1000, 0.05) : 0; previous = time;
      if (!reduce.matches) { group.rotation.y += delta * 0.045; moon.position.y = 0.45 + Math.sin(time * 0.0003) * 0.12; }
      renderer.render(scene, camera);
      if (visible && !reduce.matches && !document.hidden) frame = requestAnimationFrame(draw);
    }
    function restart() { cancelAnimationFrame(frame); previous = 0; draw(); }
    const resize = new ResizeObserver(() => { const { width, height } = target.getBoundingClientRect(); renderer.setSize(width, height); camera.aspect = width / Math.max(height, 1); camera.updateProjectionMatrix(); restart(); }); resize.observe(target);
    const intersection = new IntersectionObserver(entries => { visible = entries[0].isIntersecting; restart(); }); intersection.observe(target);
    reduce.addEventListener("change", restart); document.addEventListener("visibilitychange", restart);
    return () => { cancelAnimationFrame(frame); resize.disconnect(); intersection.disconnect(); reduce.removeEventListener("change", restart); document.removeEventListener("visibilitychange", restart); scene.traverse(object => { if (object instanceof THREE.Mesh || object instanceof THREE.Points) { object.geometry.dispose(); const materials = Array.isArray(object.material) ? object.material : [object.material]; materials.forEach(m => m.dispose()); } }); renderer.dispose(); renderer.domElement.remove(); target.classList.remove("webgl-ready"); };
  }, []);
  return <div className="orbit-canvas" ref={host} aria-hidden="true"><div className="planet-fallback"/></div>;
}
