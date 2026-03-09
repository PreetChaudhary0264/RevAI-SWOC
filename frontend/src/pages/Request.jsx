import { useState } from "react";
import { Star, Github, Linkedin, Heart, ArrowRight } from "lucide-react";

const StarAndConnect = () => {
  const [starred, setStarred] = useState(false);

  return (
    <section
      className="py-24 relative overflow-hidden"
      style={{ background: "#f7f3ee" }}
    >
      {/* Background blobs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="absolute top-[-40px] left-[15%] w-[300px] h-[300px] rounded-full opacity-20"
          style={{ background: "radial-gradient(circle, #f4a261, transparent 70%)" }}
        />
        <div
          className="absolute bottom-[-40px] right-[10%] w-[280px] h-[280px] rounded-full opacity-15"
          style={{ background: "radial-gradient(circle, #457b9d, transparent 70%)" }}
        />
      </div>

      <div className="container mx-auto px-6 relative z-10">

        {/* Section label */}
        <div className="flex justify-center mb-10">
          <div
            className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 border text-xs font-semibold tracking-widest uppercase"
            style={{ background: "#fdebd0", borderColor: "#f4a261", color: "#b5541d" }}
          >
            <Heart className="h-3.5 w-3.5" />
            Support the Project
          </div>
        </div>

        {/* Heading */}
        <div className="text-center max-w-xl mx-auto mb-14">
          <h2
            className="text-4xl md:text-5xl font-bold mb-4 leading-tight"
            style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
          >
            Like what you{" "}
            <span style={{ color: "#e76f51" }}>see?</span>
          </h2>
          <p className="text-lg leading-relaxed" style={{ color: "#4a6580" }}>
            RevAI is built with love and caffeine. If it's helped you ship better code,
            show some support — it means the world.
          </p>
        </div>

        {/* Two cards */}
        <div className="max-w-3xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* Star card */}
          <div
            className="rounded-3xl p-8 flex flex-col items-center text-center transition-all hover:-translate-y-1"
            style={{
              background: "rgba(255,255,255,0.85)",
              border: starred ? "2px solid #e76f51" : "1px solid #e8ddd2",
              backdropFilter: "blur(10px)",
              boxShadow: starred
                ? "0 8px 32px rgba(231,111,81,0.18)"
                : "0 4px 20px rgba(0,0,0,0.05)",
              transition: "all 0.3s ease",
            }}
          >
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center mb-5"
              style={{
                background: starred ? "#e76f51" : "#fdebd0",
                border: starred ? "none" : "1px solid #f4a261",
                transition: "all 0.3s ease",
              }}
            >
              <Star
                className="h-8 w-8"
                style={{
                  color: starred ? "#fff" : "#e76f51",
                  fill: starred ? "#fff" : "transparent",
                  transition: "all 0.3s ease",
                }}
              />
            </div>

            <h3
              className="text-2xl font-bold mb-2"
              style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
            >
              {starred ? "Thanks so much! 🎉" : "Star on GitHub"}
            </h3>
            <p className="text-sm leading-relaxed mb-6" style={{ color: "#4a6580" }}>
              {starred
                ? "You're awesome. Your star helps others discover RevAI."
                : "If RevAI saved you time or caught a bug, a ⭐ on GitHub goes a long way in helping others find this project."}
            </p>

            <a
              href="https://github.com/PreetChaudhary0264/RevAI-SWOC"
              target="_blank"
              rel="noopener noreferrer"
              onClick={() => setStarred(true)}
              className="w-full py-3 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all hover:opacity-90"
              style={{
                background: "#e76f51",
                color: "#fff",
                boxShadow: "0 4px 16px rgba(231,111,81,0.3)",
              }}
            >
              <Github className="h-4 w-4" />
              Star the Repo
              <ArrowRight className="h-4 w-4" />
            </a>
          </div>

          {/* LinkedIn card */}
          <div
            className="rounded-3xl p-8 flex flex-col items-center text-center transition-all hover:-translate-y-1"
            style={{
              background: "rgba(255,255,255,0.85)",
              border: "1px solid #e8ddd2",
              backdropFilter: "blur(10px)",
              boxShadow: "0 4px 20px rgba(0,0,0,0.05)",
            }}
          >
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center mb-5"
              style={{ background: "#dbeafe", border: "1px solid #93c5fd" }}
            >
              <Linkedin className="h-8 w-8" style={{ color: "#457b9d" }} />
            </div>

            <h3
              className="text-2xl font-bold mb-2"
              style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
            >
              Want to Contribute?
            </h3>
            <p className="text-sm leading-relaxed mb-6" style={{ color: "#4a6580" }}>
              Have ideas, feedback, or want to collaborate? Reach out on LinkedIn —
              whether you're a developer, designer, or just curious, let's connect.
            </p>

            <a
              href="https://www.linkedin.com/in/preet-chaudhary-5523a0306/"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full py-3 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all hover:opacity-90"
              style={{
                background: "#457b9d",
                color: "#fff",
                boxShadow: "0 4px 16px rgba(69,123,157,0.3)",
              }}
            >
              <Linkedin className="h-4 w-4" />
              Connect on LinkedIn
              <ArrowRight className="h-4 w-4" />
            </a>
          </div>
        </div>

        {/* Bottom note */}
        <div className="mt-10 max-w-md mx-auto text-center">
          <p className="text-xs leading-relaxed" style={{ color: "#6b8099" }}>
            Built solo with ❤️ by{" "}
            <a
              href="https://www.linkedin.com/in/preet-chaudhary-5523a0306/"
              target="_blank"
              rel="noopener noreferrer"
              className="font-semibold"
              style={{ color: "#e76f51" }}
            >
              Preet Chaudhary
            </a>
            . Open to feedback, collabs, and good conversations.
          </p>
        </div>

        {/* Gradient divider */}
        <div
          className="mt-14 mx-auto"
          style={{
            height: "1px",
            background: "linear-gradient(to right, transparent, #d4b896, transparent)",
            maxWidth: "400px",
          }}
        />
      </div>
    </section>
  );
};

export default StarAndConnect;