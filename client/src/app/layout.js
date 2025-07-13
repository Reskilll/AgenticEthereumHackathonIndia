import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import WagmiWrapper from "@/components/wrapper/wagmi";
import { Toaster } from "sonner";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Zero Knowledge",
  description: "Live as a true citizen, without fearing for your data",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Toaster />
        <WagmiWrapper>
          <Navbar />
          {children}
        </WagmiWrapper>
        <Footer />
      </body>
    </html>
  );
}
