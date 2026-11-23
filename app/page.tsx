import Link from "next/link";
import PilotForm from "@/components/PilotForm";
import OrbitScene from "@/components/OrbitScene";
export default function Home() {
  return <><a href="#registration" className="skip">Skip to registration</a>
    <header className="masthead"><Link href="/" className="brand" aria-label="Nova Academy home"><span className="brand-icon">✳</span><span>NOVA<span className="brand-sub">ACADEMY</span></span></Link><nav aria-label="Main navigation"><Link href="/lab">The lab ↗</Link><a href="#requirements">Flight requirements</a></nav><span className="header-tag"><i/> GATE OPEN</span></header>
    <main className="academy"><section className="mission" aria-labelledby="mission-title"><div className="mission-top"><span className="eyebrow">THE NEXT GENERATION OF EXPLORERS</span><span className="mission-no">MISSION / 012</span></div>
      <div className="mission-copy"><p className="overline"><span/> A LITTLE CURIOSITY. A BIG UNIVERSE.</p><h1 id="mission-title">Your next chapter<br/>is <em>out there.</em></h1><p>For the curious minds, the bold hearts, and the ones who always look up. Your journey starts at the gate.</p></div>
      <div className="orbital-art"><OrbitScene/><span className="orbit-label orbit-label-one">NOVA / ORBIT 01</span><span className="orbit-cross" aria-hidden="true">+</span><div className="coordinate">14° 35′ N &nbsp; 120° 58′ E<br/><span>EARTH → WHAT’S NEXT</span></div><span className="orbit-label orbit-label-two">EXPLORATION BEGINS WITH YOU</span></div>
      <div id="requirements" className="mission-bottom"><div><span className="small-label">YOUR FLIGHT CHECK</span><p>18–60 years old · A valid email · A mobile number</p></div><span className="mission-stamp" aria-hidden="true">N / A<br/>✦</span></div>
    </section>
    <section className="registration" id="registration" aria-labelledby="form-title"><div className="form-topline"><span className="eyebrow">PILOT INTAKE</span><span className="intake-badge">OPEN FOR TAKEOFF</span></div><h2 id="form-title">Become a Nova pilot.</h2><p className="form-intro">Big journeys start with a few small details.</p><PilotForm/><div className="privacy-note"><span aria-hidden="true">⌁</span><p>A learning mission. Your details are checked, then cleared.<br/>No account is created and nothing is stored.</p></div></section></main>
    <footer className="footer"><span>© {new Date().getFullYear()} NOVA ACADEMY</span><span>BUILT FOR THE ONES WHO LOOK UP ✦</span><Link href="/lab">Week 12 · Validation lab ↗</Link></footer></>;
}
