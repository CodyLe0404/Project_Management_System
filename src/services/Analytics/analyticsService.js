export const analyticsService = {
    async getStats() {
        // Simulate API Call
        await new Promise(r => setTimeout(r, 500));

        // Mock Data Response
        return [
            { title: 'Total Users', value: Math.floor(Math.random() * 10000).toString(), trend: Math.floor(Math.random() * 20) - 10 },
            { title: 'Active Sessions', value: Math.floor(Math.random() * 1000).toString(), trend: Math.floor(Math.random() * 20) - 10 },
            { title: 'Bounce Rate', value: Math.floor(Math.random() * 100) + '%', trend: Math.floor(Math.random() * 20) - 10 },
            { title: 'Revenue', value: '$' + Math.floor(Math.random() * 50000), trend: 8 }
        ];
    }
};
