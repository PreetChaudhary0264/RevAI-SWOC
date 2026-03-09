import { ArrowRight } from "lucide-react";

const steps = [
  {
    step: "01",
    title: "Connect Repository",
    description: "Link your GitHub repository with a single click. No complex setup required.",
    emoji: "📦",
  },
  {
    step: "02",
    title: "Open Pull Request",
    description: "Create a PR as usual. Our AI automatically detects new pull requests.",
    emoji: "🔄",
  },
  {
    step: "03",
    title: "AI Review",
    description: "CodeReview AI analyzes your code for bugs, security issues, and improvements.",
    emoji: "🤖",
  },
  {
    step: "04",
    title: "Get Feedback",
    description: "Receive detailed comments and suggestions directly on your PR within seconds.",
    emoji: "✅",
  },
];

const HowItWorks = () => {
  return (
    <section
      id="how-it-works"
      className="py-28 relative overflow-hidden"
      style={{ background: "#f7f3ee" }}
    >
      {/* Background blobs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="absolute top-[-40px] right-[10%] w-[320px] h-[320px] rounded-full opacity-20"
          style={{ background: "radial-gradient(circle, #457b9d, transparent 70%)" }}
        />
        <div
          className="absolute bottom-[-40px] left-[5%] w-[280px] h-[280px] rounded-full opacity-20"
          style={{ background: "radial-gradient(circle, #f4a261, transparent 70%)" }}
        />
      </div>

      <div className="container mx-auto px-6 relative z-10">

        {/* Header */}
        <div className="max-w-xl mx-auto text-center mb-20">
          <div
            className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 mb-5 border text-xs font-semibold tracking-widest uppercase"
            style={{ background: "#fdebd0", borderColor: "#f4a261", color: "#b5541d" }}
          >
            Simple Process
          </div>
          <h2
            className="text-4xl md:text-5xl font-bold mb-4 leading-tight"
            style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
          >
            How It{" "}
            <span style={{ color: "#e76f51" }}>Works</span>
          </h2>
          <p className="text-lg leading-relaxed" style={{ color: "#4a6580" }}>
            Get started in minutes with our simple 4-step process
          </p>
        </div>

        {/* Steps — horizontal timeline */}
        <div className="max-w-5xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-0 relative">

            {/* Connector line (desktop only) */}
            <div
              className="hidden md:block absolute top-10 left-[12.5%] right-[12.5%] h-px"
              style={{ background: "linear-gradient(to right, #e76f51, #457b9d)" }}
            />

            {steps.map((step, index) => (
              <div key={index} className="relative flex flex-col items-center text-center px-4">

                {/* Circle with step number */}
                <div
                  className="w-20 h-20 rounded-full flex items-center justify-center mb-5 relative z-10 text-3xl font-bold shadow-md"
                  style={{
                    background: index % 2 === 0 ? "#e76f51" : "#457b9d",
                    color: "#fff",
                    boxShadow: `0 4px 18px ${index % 2 === 0 ? "rgba(231,111,81,0.3)" : "rgba(69,123,157,0.3)"}`,
                    fontFamily: "'Georgia', serif",
                    fontSize: "1.1rem",
                  }}
                >
                  {step.step}
                </div>

                {/* Mobile arrow */}
                {index < steps.length - 1 && (
                  <ArrowRight
                    className="md:hidden mb-4 h-6 w-6"
                    style={{ color: "#e76f51", transform: "rotate(90deg)" }}
                  />
                )}

                <h3
                  className="text-lg font-bold mb-2"
                  style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
                >
                  {step.title}
                </h3>
                <p className="text-sm leading-relaxed" style={{ color: "#4a6580" }}>
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Flow diagram card */}
        <div className="mt-20 max-w-3xl mx-auto">
          <div
            className="rounded-2xl p-8"
            style={{
              background: "rgba(255,255,255,0.7)",
              border: "1px solid #e8ddd2",
              backdropFilter: "blur(8px)",
              boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
            }}
          >
            <p
              className="text-center text-xs font-semibold tracking-widest uppercase mb-8"
              style={{ color: "#b5541d" }}
            >
              Your workflow, visualized
            </p>

            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              {steps.map((step, index) => (
                <div key={index} className="flex flex-col md:flex-row items-center gap-4">
                  <div className="flex flex-col items-center gap-2">
                    <div
                      className="w-16 h-16 rounded-xl flex items-center justify-center text-2xl shadow-sm"
                      style={{
                        background: index % 2 === 0 ? "#fdebd0" : "#dbeafe",
                        border: `1px solid ${index % 2 === 0 ? "#f4a261" : "#93c5fd"}`,
                      }}
                    >
                      {step.emoji}
                    </div>
                    <span
                      className="text-xs font-semibold"
                      style={{ color: index % 2 === 0 ? "#b5541d" : "#1d4ed8" }}
                    >
                      {step.title}
                    </span>
                  </div>

                  {index < steps.length - 1 && (
                    <ArrowRight
                      className="flex-shrink-0 rotate-90 md:rotate-0"
                      style={{ color: "#d4b896" }}
                    />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Divider */}
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

export default HowItWorks;