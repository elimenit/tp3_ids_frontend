import { createLine, createPie, createHeatmap, createBar } from './charts.js';
import { initGroupByButtons, groupBy } from './groupby.js';

const canvasGraph1 = document.getElementById('graph1');

setTimeout(() => {
    createLine(canvasGraph1, data.income, 'fecha', 'ingresos', 'Recaudado', 'Evolución de Ingresos');

    initGroupByButtons((period) => {
        Chart.getChart(canvasGraph1)?.destroy(); 
        const dataAgrupada = groupBy(data.income, period, 'ingresos'); 
        console.table(dataAgrupada)
        createLine(canvasGraph1, dataAgrupada, 'fecha', 'ingresos', 'Recaudado', 'Evolución de Ingresos');
    });

    createPie(document.getElementById('graph2'), data.by_status, 'status', 'cantidad', 'Pedidos', 'Estados de Pedidos');

    createHeatmap(
        document.getElementById('graph3'), 
        data.by_hour, 
        'hora', 
        'dia', 
        'cantidad', 
        'Pedidos', 
        'Distribución Horaria de Pedidos'
    );

    createBar(
        document.getElementById('graph4'), 
        data.top_products, 
        'name', 
        'total_vendido', 
        'Ventas', 
        'Top Productos más Vendidos'
    );
    
}, 100);