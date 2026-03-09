import { Bot, Shield, Zap, GitBranch, MessageSquare, Lock } from "lucide-react";

const features = [
  {
    icon: Bot,
    title: "AI-Powered Analysis",
    description: "Advanced machine learning models analyze your code for bugs, vulnerabilities, and best practices.",
    accent: "#e76f51",
  },
  {
    icon: GitBranch,
    title: "GitHub Integration",
    description: "Seamlessly integrates with your GitHub workflow. Reviews happen automatically on every PR.",
    accent: "#457b9d",
  },
  {
    icon: MessageSquare,
    title: "Inline Comments",
    description: "Get detailed, actionable feedback directly in your pull requests, just like a human reviewer.",
    accent: "#e76f51",
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Reviews complete in seconds, not hours. Keep your development velocity high.",
    accent: "#457b9d",
  },
  {
    icon: Shield,
    title: "Security Focused",
    description: "Identifies security vulnerabilities and potential exploits before they reach production.",
    accent: "#e76f51",
  },
  {
    icon: Lock,
    title: "Private & Secure",
    description: "Your code never leaves your infrastructure. Complete privacy and security guaranteed.",
    accent: "#457b9d",
  },
];

const Features = () => {
  return (
    <section
      id="features"
      className="py-28 relative overflow-hidden"
      style={{ background: "#f7f3ee" }}
    >
      {/* Background blobs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="absolute top-[-60px] left-[-60px] w-[350px] h-[350px] rounded-full opacity-20"
          style={{ background: "radial-gradient(circle, #f4a261, transparent 70%)" }}
        />
        <div
          className="absolute bottom-[-60px] right-[-60px] w-[350px] h-[350px] rounded-full opacity-15"
          style={{ background: "radial-gradient(circle, #457b9d, transparent 70%)" }}
        />
      </div>

      <div className="container mx-auto px-6 relative z-10">

        {/* Section Header */}
        <div className="max-w-xl mx-auto text-center mb-20">
          <div
            className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 mb-5 border text-xs font-semibold tracking-widest uppercase"
            style={{ background: "#fdebd0", borderColor: "#f4a261", color: "#b5541d" }}
          >
            What's Inside
          </div>
          <h2
            className="text-4xl md:text-5xl font-bold mb-4 leading-tight"
            style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
          >
            Powerful Features for{" "}
            <span style={{ color: "#e76f51" }}>Modern Teams</span>
          </h2>
          <p className="text-lg leading-relaxed" style={{ color: "#4a6580" }}>
            Everything you need to maintain code quality and ship faster
          </p>
        </div>

        {/* Featured top row — 2 large cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {features.slice(0, 2).map((feature, index) => (
            <div
              key={index}
              className="group rounded-2xl p-8 flex gap-6 items-start transition-all hover:-translate-y-1"
              style={{
                background: "rgba(255,255,255,0.7)",
                border: "1px solid #e8ddd2",
                backdropFilter: "blur(8px)",
                boxShadow: "0 2px 16px rgba(0,0,0,0.04)",
              }}
            >
              <div
                className="flex-shrink-0 w-14 h-14 rounded-xl flex items-center justify-center transition-all group-hover:scale-110"
                style={{ background: `${feature.accent}18`, color: feature.accent }}
              >
                <feature.icon className="h-6 w-6" />
              </div>
              <div>
                <h3
                  className="text-xl font-bold mb-2"
                  style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
                >
                  {feature.title}
                </h3>
                <p className="text-base leading-relaxed" style={{ color: "#4a6580" }}>
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom row — 4 smaller cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.slice(2).map((feature, index) => (
            <div
              key={index}
              className="group rounded-2xl p-6 flex flex-col gap-4 transition-all hover:-translate-y-1"
              style={{
                background: "rgba(255,255,255,0.7)",
                border: "1px solid #e8ddd2",
                backdropFilter: "blur(8px)",
                boxShadow: "0 2px 16px rgba(0,0,0,0.04)",
              }}
            >
              <div
                className="w-11 h-11 rounded-xl flex items-center justify-center transition-all group-hover:scale-110"
                style={{ background: `${feature.accent}18`, color: feature.accent }}
              >
                <feature.icon className="h-5 w-5" />
              </div>
              <div>
                <h3
                  className="text-lg font-bold mb-1"
                  style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
                >
                  {feature.title}
                </h3>
                <p className="text-sm leading-relaxed" style={{ color: "#4a6580" }}>
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom gradient divider */}
        <div
          className="mt-20 mx-auto"
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

export default Features;