function renderizarGraficaUsuariosMes(series, categories) {
  let areaOptions = {
     series: [
       {
         name: "Usuarios registrados",
         data: series,
       },
     ],
     chart: {
       height: 350,
       type: "area",
     },
     dataLabels: {
       enabled: false,
     },
     stroke: {
       curve: "smooth",
     },
     xaxis: {
       type: "datetime",
       categories: categories,
     },
     tooltip: {
       x: {
         format: "dd/MM/yy HH:mm",
       },
     },
   };  

  let usuariosMesChart = new ApexCharts(document.querySelector('#usuarios-mes'), areaOptions)
  usuariosMesChart.render()  
}

function renderizarGraficaUsuariosDistribucion(series, labels) {
  let options = {
    series: series,
    chart: {
    type: 'donut',
  },
  labels: labels,
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
  };

  let chart = new ApexCharts(document.querySelector("#usuarios-distribucion"), options);
  chart.render();
}

function renderizarGraficaActividadUsuarios(series, labels) {
  let options = {
    series: series,
    chart: {
    type: 'donut',
  },
  labels: labels,
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
  };

  let chart = new ApexCharts(document.querySelector("#actividad-usuarios"), options);
  chart.render();
}
