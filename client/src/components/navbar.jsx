"use client";
import { Button } from "@/components/ui/button";
import { useAccount, useConnect, useDisconnect } from "wagmi";
import { metaMask } from "wagmi/connectors";
import { useState } from "react";

const connector = metaMask();

export default function Navbar() {
  const [isConnecting, setIsConnecting] = useState(false);
  const { connectAsync } = useConnect();
  const { disconnect } = useDisconnect();
  const { address, isConnected } = useAccount();

  const handleConnect = async () => {
    try {
      setIsConnecting(true);
      await connectAsync({ connector });
    } catch (err) {
      console.error("Connection failed:", err);
    } finally {
      setIsConnecting(false);
    }
  };

  return (
    <nav className="bg-black text-white p-6 flex justify-between items-center shadow-lg">
      <h1 className="text-3xl font-extrabold">ZK-DID</h1>
      {isConnected ? (
        <div className="flex items-center space-x-4">
          <span>Connected: {address.slice(0, 2)}....{address.slice(-2)}</span>
          <Button
            onClick={() => disconnect()}
            size="lg"
          >
            Disconnect
          </Button>
        </div>
      ) : (
        <Button
          size="lg"
          onClick={handleConnect}
          disabled={isConnecting}
        >
          {isConnecting ? "Connecting..." : "Connect Wallet"}
        </Button>
      )}
    </nav>
  );
}