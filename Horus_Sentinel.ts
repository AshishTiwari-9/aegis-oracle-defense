type PriceSource = () => Promise<number>;

class HorusSentinel {
    private readonly sources: PriceSource[];
    private readonly threshold: number;

    constructor(sources: PriceSource[], threshold = 0.05) {
        this.sources = sources;
        this.threshold = threshold;
    }

    async detectAnomaly(): Promise<string> {
        const prices = await this.fetchPrices();
        const median = this.calculateMedian(prices);
        const maxDeviation = this.calculateMaxDeviation(prices, median);
        
        return maxDeviation > this.threshold 
            ? `ALERT: Price deviation ${(maxDeviation * 100).toFixed(1)}% detected`
            : "Normal price activity";
    }

    private async fetchPrices(): Promise<number[]> {
        return Promise.all(this.sources.map(async source => source()));
    }

    private calculateMedian(values: number[]): number {
        const sorted = [...values].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
    }

    private calculateMaxDeviation(values: number[], median: number): number {
        return Math.max(...values.map(v => Math.abs(v - median) / median));
    }
}

// Simulation Setup
const sources: PriceSource[] = [
    () => Promise.resolve(100),   // Normal source
    () => Promise.resolve(102),   // Normal source
    () => Promise.resolve(150)    // Malicious source
];

// Execution
(async () => {
    const monitor = new HorusSentinel(sources);
    const result = await monitor.detectAnomaly();
    console.log("Horus Sentinel Results:");
    console.log(result);
})();
