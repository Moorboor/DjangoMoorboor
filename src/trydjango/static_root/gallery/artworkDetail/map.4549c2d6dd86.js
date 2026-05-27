(async () => {
  const mapElement = document.getElementById('map');
  if (!mapElement) return;

  const coordsJson = document.getElementById('coords-json');
  if (!coordsJson) return;

  const coords = JSON.parse(coordsJson.textContent);
  const [lat, lng] = coords.split(",").map(Number);

  const map = L.map('map').setView([lat, lng], 12);

  // Satellite layer
  L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    {attribution: '&copy; Esri', maxZoom: 19}
  ).addTo(map);

  // Labels layer
  L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
    {attribution: '&copy; Esri', maxZoom: 19}
  ).addTo(map);

  // Current artwork marker
  L.marker([lat, lng])
    .addTo(map)
    .bindPopup(`<strong style="color:white;">Current Artwork Location</strong>`);
})();