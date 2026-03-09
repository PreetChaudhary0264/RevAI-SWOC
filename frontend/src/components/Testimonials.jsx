import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { Star, Quote } from "lucide-react";

const testimonials = [
  {
    name: "Sarah Chen",
    role: "Senior Developer",
    company: "TechCorp",
    avatar: "SC",
    content:
      "RevAI has transformed our code review process. It catches issues we would have missed and provides valuable suggestions. Our code quality has improved significantly.",
    rating: 5,
    accent: "#e76f51",
  },
  {
    name: "Michael Rodriguez",
    role: "Engineering Manager",
    company: "StartupXYZ",
    avatar: "MR",
    content:
      "The speed and accuracy are incredible. What used to take hours now happens in seconds. It's like having an expert reviewer available 24/7.",
    rating: 5,
    accent: "#457b9d",
  },
  {
    name: "Emily Watson",
    role: "Tech Lead",
    company: "DevStudio",
    avatar: "EW",
    content:
      "Integration was seamless and the insights are spot-on. The security vulnerability detection alone has saved us from potential disasters.",
    rating: 5,
    accent: "#e76f51",
  },
  {
    name: "James Kumar",
    role: "Full Stack Developer",
    company: "CloudNative Inc",
    avatar: "JK",
    content:
      "Best investment we've made in our development workflow. The AI understands context and provides meaningful feedback, not just generic suggestions.",
    rating: 5,
    accent: "#457b9d",
  },
  {
    name: "Lisa Park",
    role: "CTO",
    company: "InnovateLabs",
    avatar: "LP",
    content:
      "Our team velocity increased by 40% after implementing RevAI. It's an essential tool for any modern development team.",
    rating: 5,
    accent: "#e76f51",
  },
  {
    name: "David Thompson",
    role: "Software Architect",
    company: "Enterprise Solutions",
    avatar: "DT",
    content:
      "The inline comments are incredibly detailed and actionable. It's like having a senior developer review every line of code.",
    rating: 5,
    accent: "#457b9d",
  },
];

const Testimonials = () => {
  const featured = testimonials[0];
  const rest = testimonials.slice(1);

  return (
    <section
      id="testimonials"
      className="py-28 relative overflow-hidden"
      style={{ background: "#f7f3ee" }}
    >
      {/* Background blobs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="absolute top-[10%] right-[-80px] w-[360px] h-[360px] rounded-full opacity-20"
          style={{ background: "radial-gradient(circle, #e76f51, transparent 70%)" }}
        />
        <div
          className="absolute bottom-[5%] left-[-60px] w-[300px] h-[300px] rounded-full opacity-15"
          style={{ background: "radial-gradient(circle, #457b9d, transparent 70%)" }}
        />
      </div>

      <div className="container mx-auto px-6 relative z-10">

        {/* Header */}
        <div className="max-w-xl mx-auto text-center mb-16">
          <div
            className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 mb-5 border text-xs font-semibold tracking-widest uppercase"
            style={{ background: "#fdebd0", borderColor: "#f4a261", color: "#b5541d" }}
          >
            Testimonials
          </div>
          <h2
            className="text-4xl md:text-5xl font-bold mb-4 leading-tight"
            style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
          >
            Loved by{" "}
            <span style={{ color: "#e76f51" }}>Developers</span>{" "}
            Worldwide
          </h2>
          <p className="text-lg leading-relaxed" style={{ color: "#4a6580" }}>
            Join thousands of developers who trust RevAI
          </p>
        </div>

        {/* Featured large testimonial */}
        <div className="max-w-3xl mx-auto mb-10">
          <div
            className="rounded-3xl p-10 relative overflow-hidden"
            style={{
              background: "rgba(255,255,255,0.85)",
              border: "1px solid #e8ddd2",
              backdropFilter: "blur(10px)",
              boxShadow: "0 8px 40px rgba(231,111,81,0.10)",
            }}
          >
            {/* Giant quote mark */}
            <Quote
              className="absolute top-6 right-8 opacity-10"
              style={{ color: "#e76f51", width: 80, height: 80 }}
            />

            {/* Stars */}
            <div className="flex gap-1 mb-6">
              {[...Array(featured.rating)].map((_, i) => (
                <Star key={i} className="h-5 w-5" style={{ fill: "#e76f51", color: "#e76f51" }} />
              ))}
            </div>

            <p
              className="text-2xl leading-relaxed mb-8 font-medium"
              style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
            >
              "{featured.content}"
            </p>

            <div className="flex items-center gap-4">
              <div
                className="w-14 h-14 rounded-full flex items-center justify-center text-white font-bold text-lg flex-shrink-0"
                style={{ background: "#e76f51", fontFamily: "'Georgia', serif" }}
              >
                {featured.avatar}
              </div>
              <div>
                <div
                  className="font-bold text-lg"
                  style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
                >
                  {featured.name}
                </div>
                <div className="text-sm" style={{ color: "#4a6580" }}>
                  {featured.role}{" "}
                  <span style={{ color: "#e76f51" }}>@{featured.company}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Remaining 5 cards in a staggered grid */}
        <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-5">
          {rest.map((t, index) => (
            <div
              key={index}
              className="group rounded-2xl p-6 flex flex-col gap-4 transition-all hover:-translate-y-1"
              style={{
                background: "rgba(255,255,255,0.7)",
                border: "1px solid #e8ddd2",
                backdropFilter: "blur(8px)",
                boxShadow: "0 2px 16px rgba(0,0,0,0.04)",
                marginTop: index === 1 ? "24px" : "0",
              }}
            >
              {/* Stars */}
              <div className="flex gap-1">
                {[...Array(t.rating)].map((_, i) => (
                  <Star
                    key={i}
                    className="h-3.5 w-3.5"
                    style={{ fill: t.accent, color: t.accent }}
                  />
                ))}
              </div>

              {/* Quote */}
              <p
                className="text-sm leading-relaxed flex-1"
                style={{ color: "#4a6580" }}
              >
                "{t.content}"
              </p>

              {/* Author */}
              <div className="flex items-center gap-3 pt-2" style={{ borderTop: "1px solid #f0e8df" }}>
                <div
                  className="w-9 h-9 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0"
                  style={{ background: t.accent }}
                >
                  {t.avatar}
                </div>
                <div>
                  <div
                    className="text-sm font-bold"
                    style={{ color: "#1d3557" }}
                  >
                    {t.name}
                  </div>
                  <div className="text-xs" style={{ color: "#6b8099" }}>
                    {t.role} · {t.company}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom strip — social proof */}
        <div
          className="mt-16 max-w-2xl mx-auto rounded-2xl px-8 py-5 flex flex-col sm:flex-row items-center justify-between gap-4"
          style={{
            background: "rgba(255,255,255,0.7)",
            border: "1px solid #e8ddd2",
          }}
        >
          <div className="flex -space-x-3">
            {testimonials.map((t, i) => (
              <div
                key={i}
                className="w-9 h-9 rounded-full flex items-center justify-center text-white text-xs font-bold border-2 border-white"
                style={{ background: t.accent }}
              >
                {t.avatar}
              </div>
            ))}
          </div>
          <p className="text-sm text-center" style={{ color: "#4a6580" }}>
            <span className="font-bold" style={{ color: "#1d3557" }}>1,200+ developers</span> already shipping better code with RevAI
          </p>
          <div className="flex gap-1">
            {[...Array(5)].map((_, i) => (
              <Star key={i} className="h-4 w-4" style={{ fill: "#e76f51", color: "#e76f51" }} />
            ))}
          </div>
        </div>

        {/* Divider */}
        <div
          className="mt-16 mx-auto"
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

export default Testimonials;