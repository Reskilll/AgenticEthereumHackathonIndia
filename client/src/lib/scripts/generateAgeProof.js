import * as snarkjs from "snarkjs";

/**
 * Generate a ZK age proof that the user is >= 18 as of referenceYear, bound to a unique challenge.
 * @param {string|Date} dob - Date of birth (string or Date object)
 * @param {number} referenceYear - The year to compare against (e.g., current year)
 * @param {string|number|bigint} challenge - Unique challenge/nonce/sessionId (should be public and random)
 * @returns {Promise<object>} ZK proof object
 */


export async function generateAgeProof(dob, referenceYear, challenge) {
  // Sanitize and check DOB
  if (!dob || isNaN(new Date(dob))) {
    throw new Error("Invalid date of birth format.");
  }

  const dobYear = new Date(dob).getUTCFullYear();
  if (dobYear < 1900 || dobYear > referenceYear) {
    throw new Error("Unrealistic year of birth.");
  }

  // TODO: make sure these files are "not tampered" with, implementing checksumming or signing would be a good idea
  const wasmUrl = "/api/snark-artifacts/age.wasm";
  const zkeyUrl = "/api/snark-artifacts/age_final.zkey";

  const [wasmResp, zkeyResp] = await Promise.all([
    fetch(wasmUrl, { method: "HEAD" }),
    fetch(zkeyUrl, { method: "HEAD" }),
  ]);

  console.log("wasmResp: " + wasmResp + "\nzkeyResp: " + zkeyResp);

  if (!wasmResp.ok) {
    throw new Error("Missing or inaccessible age.wasm. Did you compile the circuit?");
  }

  if (!zkeyResp.ok) {
    throw new Error("Missing or inaccessible age_final.zkey. Did you run compile-circuits?");
  }

  const input = {
    dobYear: dobYear,          
    referenceYear,     
    challenge          
  };

  try {
    const { proof, publicSignals } = await snarkjs.groth16.fullProve(input, wasmUrl, zkeyUrl);
    console.log("proof: " + proof);

    return {
      protocol: "groth16",
      curve: "bn128",
      pi_a: proof.pi_a,
      pi_b: proof.pi_b,
      pi_c: proof.pi_c,
      publicSignals
    };
  } catch (err) {
    throw new Error("Proof generation failed: " + err.message);
  }
}