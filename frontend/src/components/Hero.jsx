import { Button } from "./ui/button";
import { Link } from "react-router-dom";
import { ArrowRight, Github, Sparkles } from "lucide-react";

const Hero = () => {
  return (
    <section
      className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20"
      style={{ background: "#f7f3ee" }}
    >
      {/* Background blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div
          className="absolute top-[-80px] right-[-80px] w-[480px] h-[480px] rounded-full opacity-30"
          style={{ background: "radial-gradient(circle, #f4a261, transparent 70%)" }}
        />
        <div
          className="absolute bottom-[-60px] left-[-60px] w-[400px] h-[400px] rounded-full opacity-20"
          style={{ background: "radial-gradient(circle, #457b9d, transparent 70%)" }}
        />
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] rounded-full opacity-10"
          style={{ background: "radial-gradient(ellipse, #e76f51, transparent 70%)" }}
        />
      </div>

      <div className="container mx-auto px-6 relative z-10">
        <div className="max-w-3xl mx-auto text-center">

          {/* Badge */}
          <div
            className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 mb-8 border"
            style={{
              background: "#fdebd0",
              borderColor: "#f4a261",
            }}
          >
            <Sparkles className="h-3.5 w-3.5" style={{ color: "#e76f51" }} />
            <span
              className="text-xs font-semibold tracking-widest uppercase"
              style={{ color: "#b5541d" }}
            >
              AI-Powered Code Review
            </span>
          </div>

          {/* Main Heading */}
          <h1
            className="text-5xl md:text-6xl font-bold mb-5 leading-tight"
            style={{
              color: "#1d3557",
              fontFamily: "'Georgia', serif",
              letterSpacing: "-0.02em",
            }}
          >
            Automated Code Reviews
            <br />
            <span style={{ color: "#e76f51" }}>Right in Your PRs</span>
          </h1>

          {/* Subheading */}
          <p
            className="text-lg mb-10 max-w-xl mx-auto leading-relaxed"
            style={{ color: "#4a6580" }}
          >
            Connect your GitHub repository and let AI review your code, catch bugs,
            and add insightful comments directly on your pull requests.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button
              variant="hero"
              size="lg"
              className="group font-semibold px-7 py-3 rounded-xl transition-all hover:opacity-90"
              style={{
                background: "#e76f51",
                color: "#fff",
                boxShadow: "0 4px 18px rgba(231,111,81,0.35)",
              }}
              asChild
            >
              <Link to="/get-started">
                Get Started Free
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </Button>

              <a 
                 href="https://github.com/PreetChaudhary0264/RevAI-A" 
                 target="_blank" 
                 rel="noopener noreferrer"
               >
                 <Button
                   variant="outline"
                   size="lg"
                   className="group font-semibold px-7 py-3 rounded-xl transition-all"
                   style={{
                     background: "transparent",
                     border: "1.5px solid #457b9d",
                     color: "#457b9d",
                   }}
                 >
                   <Github className="mr-2 h-4 w-4" />
                   View on GitHub
                 </Button>
               </a>
          </div>

          {/* Divider */}
          <div
            className="mt-16 mb-10 mx-auto"
            style={{
              height: "1px",
              background: "linear-gradient(to right, transparent, #d4b896, transparent)",
              maxWidth: "400px",
            }}
          />

          {/* Stats */}
          <div
            className="grid grid-cols-3 gap-8 max-w-lg mx-auto rounded-2xl px-8 py-6"
            style={{
              background: "rgba(255,255,255,0.6)",
              border: "1px solid #e8ddd2",
              backdropFilter: "blur(8px)",
            }}
          >
            <div>
              <div
                className="text-3xl font-bold mb-1"
                style={{ color: "#e76f51", fontFamily: "'Georgia', serif" }}
              >
                10+
              </div>
              <div className="text-sm" style={{ color: "#6b8099" }}>Reviews Done</div>
            </div>
            <div>
              <div
                className="text-3xl font-bold mb-1"
                style={{ color: "#e76f51", fontFamily: "'Georgia', serif" }}
              >
                50+
              </div>
              <div className="text-sm" style={{ color: "#6b8099" }}>Active Users</div>
            </div>
            <div>
              <div
                className="text-3xl font-bold mb-1"
                style={{ color: "#e76f51", fontFamily: "'Georgia', serif" }}
              >
                80.0%
              </div>
              <div className="text-sm" style={{ color: "#6b8099" }}>Accuracy</div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

export default Hero;