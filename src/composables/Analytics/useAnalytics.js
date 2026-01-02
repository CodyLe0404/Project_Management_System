import { ref } from 'vue';
import { analyticsService } from '../../services/Analytics/analyticsService';

export function useAnalytics() {
    const stats = ref([
        { title: 'Total Users', value: '12,345', trend: 12 },
        { title: 'Active Sessions', value: '843', trend: -5 },
        { title: 'Bounce Rate', value: '42%', trend: -2 },
        { title: 'Revenue', value: '$45,200', trend: 8 }
    ]);

    const loading = ref(false);

    const refreshStats = async () => {
        try {
            loading.value = true;
            const data = await analyticsService.getStats();
            stats.value = data;
        } catch (e) {
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    return {
        stats,
        loading,
        refreshStats
    };
}
