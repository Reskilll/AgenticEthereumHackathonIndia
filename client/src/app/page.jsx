"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, Shield, Eye, Lock, Zap, CheckCircle, Users } from "lucide-react";
import { useRouter } from "next/navigation";
import { useAccount } from "wagmi";
import { toast } from "sonner";

export default function Home() {
  const { address, isConnected } = useAccount();
  const router = useRouter();
  
  const handleGetStarted = () => {
    if (!isConnected) {
      toast("Please connect your wallet first!");
      return;
    }
    router.push("/user/upload");
  };

  return (
    <div className="min-h-screen bg-background">
      
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          <Badge variant="outline" className="mb-4">
            <Shield className="w-4 h-4 mr-2" />
            Zero-Knowledge Identity Verification
          </Badge>
          
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            Decentralized Identity Verification
            <br />
            <span className="text-muted-foreground">with ZK-SNARKs</span>
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Empowering users to verify their identity without revealing private data.
            Harness the power of zero-knowledge proofs for privacy and security.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" onClick={handleGetStarted} className="text-lg">
              Get Started
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
            <Button variant="outline" size="lg" className="text-lg">
              Learn More
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Why Choose ZK-DID?
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Experience the future of digital identity with cutting-edge cryptographic technology
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              icon: Shield,
              title: "Military-Grade Security",
              description: "Advanced zk-SNARK protocols ensure your data remains cryptographically secure"
            },
            {
              icon: Eye,
              title: "Complete Privacy",
              description: "Verify your identity without exposing any personal information"
            },
            {
              icon: Lock,
              title: "Self-Sovereign Identity",
              description: "You own and control your digital identity, not corporations"
            },
            {
              icon: Zap,
              title: "Lightning Fast",
              description: "Instant verification with minimal computational overhead"
            },
            {
              icon: Users,
              title: "Universal Compatibility",
              description: "Works with any blockchain and identity verification system"
            },
            {
              icon: CheckCircle,
              title: "Mathematically Proven",
              description: "Zero-knowledge proofs provide mathematical certainty"
            }
          ].map((feature, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-muted/50 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              How It Works
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Three simple steps to secure, private identity verification
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Upload Documents",
                description: "Securely upload your identity documents to generate cryptographic proofs"
              },
              {
                step: "02",
                title: "Generate Proof",
                description: "Our zk-SNARK system creates a mathematical proof of your identity"
              },
              {
                step: "03",
                title: "Verify Instantly",
                description: "Share your proof with anyone while keeping your data completely private"
              }
            ].map((step, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-primary-foreground font-bold text-xl">
                      {step.step}
                    </span>
                  </div>
                  <CardTitle className="text-2xl">{step.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {step.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <h2 className="text-3xl md:text-4xl font-bold">
              Privacy-First Identity
            </h2>
            <p className="text-lg text-muted-foreground">
              Traditional identity verification systems require you to share sensitive personal 
              information. ZK-DID changes this by using zero-knowledge proofs to verify your 
              identity without revealing any personal data.
            </p>
            <div className="space-y-4">
              {[
                "No personal data stored on servers",
                "Cryptographically secure verification",
                "Decentralized and censorship-resistant",
                "Compatible with Web3 ecosystem"
              ].map((benefit, index) => (
                <div key={index} className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span>{benefit}</span>
                </div>
              ))}
            </div>
          </div>
          
          <Card className="p-8">
            <div className="space-y-6">
              <div className="text-center">
                <Shield className="w-16 h-16 mx-auto mb-4 text-primary" />
                <h3 className="text-2xl font-bold mb-2">Zero-Knowledge Proofs</h3>
                <p className="text-muted-foreground">
                  Prove you know something without revealing what you know
                </p>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-center">
                <div className="space-y-2">
                  <div className="text-2xl font-bold text-green-600">100%</div>
                  <div className="text-sm text-muted-foreground">Privacy Protected</div>
                </div>
                <div className="space-y-2">
                  <div className="text-2xl font-bold text-blue-600">0</div>
                  <div className="text-sm text-muted-foreground">Data Stored</div>
                </div>
                <div className="space-y-2">
                  <div className="text-2xl font-bold text-purple-600">∞</div>
                  <div className="text-sm text-muted-foreground">Security Level</div>
                </div>
                <div className="space-y-2">
                  <div className="text-2xl font-bold text-orange-600">&lt;5s</div>
                  <div className="text-sm text-muted-foreground">Verification Time</div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-muted/50 py-20">
        <div className="container mx-auto px-4 text-center">
          <Card className="max-w-3xl mx-auto p-8">
            <CardHeader>
              <CardTitle className="text-3xl md:text-4xl mb-4">
                Ready to Take Control of Your Identity?
              </CardTitle>
              <CardDescription className="text-lg">
                Join the privacy revolution and experience true self-sovereign identity
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="lg" onClick={handleGetStarted} className="text-lg">
                  Start Your Journey
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
                <Button variant="outline" size="lg" className="text-lg">
                  View Documentation
                </Button>
              </div>
              
              <div className="flex flex-wrap justify-center gap-4 pt-4">
                <Badge variant="secondary">Web3 Compatible</Badge>
                <Badge variant="secondary">Open Source</Badge>
                <Badge variant="secondary">Decentralized</Badge>
                <Badge variant="secondary">Privacy-First</Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
}