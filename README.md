# Aegis: Multi-Layered DeFi Security Framework

Aegis is a proof-of-concept security system designed to prevent and mitigate oracle manipulation attacks in decentralized finance (DeFi) protocols. It combines pre-deployment static analysis, real-time anomaly detection, and decentralized emergency response.

---

## Components

- **Thoth Analyzer**: Python-based static and AI-augmented vulnerability scanner for Solidity smart contracts.
- **Horus Sentinel**: TypeScript-based real-time price deviation and anomaly detector.
- **Anubis Response Module**: Solidity smart contract for on-chain emergency pausing (PoC only).

---

## Quick Start

### 1. Thoth Analysis Engine

**Requirements:**
- Python 3.11+
- OpenAI API key (set as `OPENAI_API_KEY` in your environment)
- `KiloPriceFeed.sol` in the same directory (demo vulnerable contract)

**Install dependencies:**
```
pip install -r requirements.txt
```


**Run static and LLM analysis:**
```
export OPENAI_API_KEY=your-openai-api-key
python3 Thoth_Analyzer.py
```


---

### 2. Horus Sentinel

**Requirements:**
- Node.js v20+
- npm

**Install dependencies:**
```
npm install
```


**Run real-time monitoring:**
```
npm start
```

---

### 3. Anubis Response Module

The Solidity contracts (`AnubisResponse.sol`, `AegisAutomation.sol`) are provided for demonstration and reference only. Full on-chain integration requires a Chainlink Automation setup and a deployed DeFi protocol.

---

## Notes

- **Thoth Analyzer** uses GPT-4o for demonstration, but can be configured for custom or local LLMs. Ensure `KiloPriceFeed.sol` (a simplified version of the exploited KiloEx contract) is present in the root directory for analysis.
- **Horus Sentinel** is modular and can be extended to detect flash loan attacks with further development.
- The Solidity contracts are for PoC and are not intended for direct deployment to production environments without further dev/security review and integration.

---

## License

MIT License

---

## Acknowledgements

- OpenAI for LLM APIs
- Slither for static analysis tooling
- Chainlink for decentralized automation infrastructure
