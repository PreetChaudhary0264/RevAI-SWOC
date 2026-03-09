import { Code2, Github, Twitter, Linkedin, Mail } from "lucide-react";
import { Button } from "./ui/button";

const Footer = () => {
  return (
    <footer style={{ background: "#1d3557", borderTop: "3px solid #e76f51" }} className="py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">

          {/* Brand */}
          <div className="md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: "#e76f51" }}>
                <Code2 className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white" style={{ fontFamily: "'Georgia', serif" }}>RevAI</span>
            </div>
            <p className="text-sm leading-relaxed" style={{ color: "#a8bfcf" }}>
              Automated code reviews powered by AI. Ship faster with confidence.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-bold mb-4 text-sm tracking-widest uppercase" style={{ color: "#e76f51" }}>Product</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#features" style={{ color: "#a8bfcf" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#a8bfcf"} className="transition-colors">Features</a></li>
              <li><a href="#how-it-works" style={{ color: "#a8bfcf" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#a8bfcf"} className="transition-colors">How It Works</a></li>
              <li><a href="#" style={{ color: "#a8bfcf" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#a8bfcf"} className="transition-colors">Pricing</a></li>
              <li><a href="#" style={{ color: "#a8bfcf" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#a8bfcf"} className="transition-colors">Documentation</a></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-bold mb-4 text-sm tracking-widest uppercase" style={{ color: "#457b9d" }}>Company</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#" style={{ color: "#a8bfcf" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#a8bfcf"} className="transition-colors">About</a></li>
              <li><a href="#" style={{ color: "#a8bfcf" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#a8bfcf"} className="transition-colors">Blog</a></li>
              <li><a href="#" style={{ color: "#a8bfcf" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#a8bfcf"} className="transition-colors">Careers</a></li>
              <li><a href="#" style={{ color: "#a8bfcf" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#a8bfcf"} className="transition-colors">Contact</a></li>
            </ul>
          </div>

          {/* Connect */}
          <div>
            <h3 className="font-bold mb-4 text-sm tracking-widest uppercase" style={{ color: "#e76f51" }}>Connect</h3>
            <div className="flex gap-3">
              <Button variant="ghost" size="icon" className="rounded-lg transition-all" style={{ background: "rgba(255,255,255,0.08)", border: "1px solid rgba(255,255,255,0.12)", color: "#a8bfcf" }} asChild>
                <a href="https://github.com/PreetChaudhary0264" target="_blank" rel="noopener noreferrer">
                  <Github className="h-5 w-5" />
                </a>
              </Button>
              <Button variant="ghost" size="icon" className="rounded-lg transition-all" style={{ background: "rgba(255,255,255,0.08)", border: "1px solid rgba(255,255,255,0.12)", color: "#a8bfcf" }} asChild>
                <a href="https://x.com/PreetSi11143247" target="_blank" rel="noopener noreferrer">
                  <Twitter className="h-5 w-5" />
                </a>
              </Button>
              <Button variant="ghost" size="icon" className="rounded-lg transition-all" style={{ background: "rgba(255,255,255,0.08)", border: "1px solid rgba(255,255,255,0.12)", color: "#a8bfcf" }} asChild>
                <a href="https://www.linkedin.com/in/preet-chaudhary-5523a0306/" target="_blank" rel="noopener noreferrer">
                  <Linkedin className="h-5 w-5" />
                </a>
              </Button>
            </div>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-sm" style={{ borderTop: "1px solid rgba(255,255,255,0.08)", color: "#6b8099" }}>
          <p>© 2025 <span style={{ color: "#f4a261", fontFamily: "'Georgia', serif" }}>RevAI</span>. All rights reserved.</p>
          <div className="flex gap-6">
            <a href="#" style={{ color: "#6b8099" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#6b8099"} className="transition-colors">Privacy Policy</a>
            <a href="#" style={{ color: "#6b8099" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#6b8099"} className="transition-colors">Terms of Service</a>
            <a href="#" style={{ color: "#6b8099" }} onMouseEnter={e => e.currentTarget.style.color = "#f4a261"} onMouseLeave={e => e.currentTarget.style.color = "#6b8099"} className="transition-colors">Security</a>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;