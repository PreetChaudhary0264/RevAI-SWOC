import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Code2, Github, ArrowRight, CheckCircle2, Star } from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { toast } from "react-toastify";
import StarAndConnect from "./Request";

const GetStarted = () => {
  const [repoUrl, setRepoUrl] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!repoUrl.trim()) {
      toast.error("Please enter a GitHub repository URL");
      return;
    }

    const githubPattern = /^https?:\/\/(www\.)?github\.com\/([\w-]+)\/([\w.-]+)(\/)?$/;
    const match = repoUrl.match(githubPattern);
    if (!match) {
      toast.error("Please enter a valid GitHub repository URL");
      return;
    }

    const owner = match[2];
    const repo = match[3];

    setIsSubmitting(true);

    try {
      const checkResponse = await fetch(`https://api.github.com/repos/${owner}/${repo}`);
      if (checkResponse.status === 404) {
        toast.error("Repository not found or private");
        setIsSubmitting(false);
        return;
      }

      const prResponse = await fetch(
        `https://api.github.com/repos/${owner}/${repo}/pulls?state=open&sort=created&direction=desc`
      );
      const prData = await prResponse.json();

      if (!Array.isArray(prData) || prData.length === 0) {
        toast.error("No open pull requests found in this repository");
        setIsSubmitting(false);
        return;
      }

      const pr_number = prData[0].number;
      console.log("Latest PR number:", pr_number);

      const response = await fetch("http://127.0.0.1:5000/review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repo_url: repoUrl,
          pr_number: pr_number,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        toast.error(data.error || "Failed to submit repository");
        return;
      }

      const { task_id } = data;

      let toastId = toast.loading("🕓 Task queued. Waiting to start review...");

      const pollInterval = setInterval(async () => {
        try {
          const statusRes = await fetch(`http://127.0.0.1:5000/status/${task_id}`);
          const statusData = await statusRes.json();

          if (statusData.status === "pending") {
            toast.update(toastId, {
              render: "⏳ Waiting in queue...",
              type: "info",
              isLoading: true,
            });
          } else if (
            statusData.status === "in_progress" ||
            statusData.status === "progress" ||
            statusData.status === "started"
          ) {
            toast.update(toastId, {
              render: `🔍 ${statusData.message || "Reviewing..."}`,
              type: "info",
              isLoading: true,
            });
          } else if (statusData.status === "completed") {
            toast.update(toastId, {
              render: "✅ Review completed successfully!",
              type: "success",
              isLoading: false,
              autoClose: 3000,
            });
            clearInterval(pollInterval);
          } else if (statusData.status === "failed") {
            toast.update(toastId, {
              render: `❌ Review failed: ${statusData.message}`,
              type: "error",
              isLoading: false,
              autoClose: 4000,
            });
            clearInterval(pollInterval);
          }
        } catch (err) {
          toast.update(toastId, {
            render: "⚠️ Lost connection to backend",
            type: "error",
            isLoading: false,
            autoClose: 4000,
          });
          clearInterval(pollInterval);
        }
      }, 4000);

      setRepoUrl("");
    } catch (error) {
      console.error(error);
      toast.error("Error connecting to backend");
    } finally {
      setIsSubmitting(false);
    }
  };

  const features = [
    "AI-powered code analysis",
    "Automated PR comments",
    "Security vulnerability detection",
    "Best practices suggestions",
  ];

  return (
    <>
    <div
      className="min-h-screen flex flex-col"
      style={{ background: "#f7f3ee", color: "#1d3557" }}
    >
      {/* Navbar */}
      <nav
        className="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg"
        style={{
          background: "rgba(247,243,238,0.85)",
          borderBottom: "1px solid #e8ddd2",
        }}
      >
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate("/")}
              className="flex items-center gap-2 hover:opacity-80 transition-opacity"
            >
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center"
                style={{ background: "#e76f51" }}
              >
                <Code2 className="h-5 w-5 text-white" />
              </div>
              <span
                className="text-xl font-bold"
                style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
              >
                RevAI
              </span>
            </button>
            <Button
              variant="ghost"
              onClick={() => navigate("/")}
              className="font-medium transition-colors"
              style={{ color: "#457b9d" }}
            >
              Back to Home
            </Button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 pt-24 pb-16">
        <div className="w-full max-w-4xl">
          <div className="text-center mb-8 animate-fade-in">
            <div
              className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-6 border text-xs font-semibold tracking-widest uppercase"
              style={{
                background: "#fdebd0",
                borderColor: "#f4a261",
                color: "#b5541d",
              }}
            >
              <Github className="h-4 w-4" />
              <span>Connect Your Repository</span>
            </div>

            <h1
              className="text-4xl md:text-5xl font-bold mb-4"
              style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
            >
              Start Your Code Review
            </h1>
            <p
              className="text-lg max-w-2xl mx-auto leading-relaxed"
              style={{ color: "#4a6580" }}
            >
              Paste your GitHub repository URL below and let our AI review your
              code, identify issues, and provide intelligent feedback on your
              pull requests.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6 animate-scale-in">
            {/* Form Card */}
            <Card
              className="shadow-xl"
              style={{
                background: "rgba(255,255,255,0.75)",
                border: "1px solid #e8ddd2",
                backdropFilter: "blur(8px)",
              }}
            >
              <CardHeader>
                <CardTitle
                  className="flex items-center gap-2"
                  style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
                >
                  <Github className="h-5 w-5" style={{ color: "#e76f51" }} />
                  Repository Details
                </CardTitle>
                <CardDescription style={{ color: "#6b8099" }}>
                  Enter your GitHub repository URL to get started
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <Label
                      htmlFor="repo-url"
                      style={{ color: "#1d3557", fontWeight: "600" }}
                    >
                      GitHub Repository URL
                    </Label>
                    <Input
                      id="repo-url"
                      type="url"
                      placeholder="https://github.com/username/repository"
                      value={repoUrl}
                      onChange={(e) => setRepoUrl(e.target.value)}
                      className="h-12"
                      style={{
                        background: "#f7f3ee",
                        border: "1px solid #e8ddd2",
                        color: "#1d3557",
                      }}
                      disabled={isSubmitting}
                    />
                    <p className="text-xs" style={{ color: "#6b8099" }}>
                      Example: https://github.com/facebook/react
                    </p>
                  </div>

                  <Button
                    type="submit"
                    className="w-full font-semibold transition-all"
                    style={{
                      background: "#e76f51",
                      color: "#fff",
                      boxShadow: "0 4px 18px rgba(231,111,81,0.3)",
                    }}
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? (
                      "Submitting..."
                    ) : (
                      <>
                        Start Review
                        <ArrowRight className="h-4 w-4 ml-2" />
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Features Card */}
            <Card
              style={{
                background: "rgba(255,255,255,0.6)",
                border: "1px solid #e8ddd2",
                backdropFilter: "blur(8px)",
              }}
            >
              <CardHeader>
                <CardTitle
                  style={{ color: "#1d3557", fontFamily: "'Georgia', serif" }}
                >
                  What You'll Get
                </CardTitle>
                <CardDescription style={{ color: "#6b8099" }}>
                  Our AI-powered review includes
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {features.map((feature, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <CheckCircle2
                        className="h-5 w-5 mt-0.5 flex-shrink-0"
                        style={{ color: "#e76f51" }}
                      />
                      <span className="text-sm" style={{ color: "#4a6580" }}>
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>

                <div
                  className="mt-6 p-4 rounded-lg"
                  style={{
                    background: "#fdebd0",
                    border: "1px solid #f4a261",
                  }}
                >
                  <p className="text-sm" style={{ color: "#4a6580" }}>
                    <strong style={{ color: "#b5541d" }}>Pro Tip:</strong> Make
                    sure your repository has open pull requests for the AI to
                    review and comment on.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Additional Info */}
          <div className="mt-8 text-center">
            <p className="text-sm" style={{ color: "#6b8099" }}>
              By submitting your repository, you agree to our terms of service
              and privacy policy.
            </p>
          </div>
        </div>
      </main>
    </div>

    <StarAndConnect/>
    </>
  );
};

export default GetStarted;

