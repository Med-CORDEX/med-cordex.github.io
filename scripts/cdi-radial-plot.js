let CID_DATA = null;

const width = 600;
const height = 600;
const radius = 250;

const container = document.getElementById("cid-radial-plot");

const svg = document.createElementNS(
  "http://www.w3.org/2000/svg",
  "svg"
);

svg.setAttribute("width", width);
svg.setAttribute("height", height);

container.appendChild(svg);

const centerX = width / 2;
const centerY = height / 2;

function polarToCartesian(r, angleDeg) {

  const angle = (angleDeg - 90) * Math.PI / 180;

  return {
    x: centerX + r * Math.cos(angle),
    y: centerY + r * Math.sin(angle)
  };

}

function drawSector(
  rOuter,
  rInner,
  angle1,
  angle2,
  color
) {

  const p1 = polarToCartesian(rOuter, angle1);
  const p2 = polarToCartesian(rOuter, angle2);
  const p3 = polarToCartesian(rInner, angle2);
  const p4 = polarToCartesian(rInner, angle1);

  const path = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "path"
  );

  const d = `
    M ${p1.x} ${p1.y}
    A ${rOuter} ${rOuter} 0 0 1 ${p2.x} ${p2.y}
    L ${p3.x} ${p3.y}
    A ${rInner} ${rInner} 0 0 0 ${p4.x} ${p4.y}
    Z
  `;

  path.setAttribute("d", d);
  path.setAttribute("fill", color);
  path.setAttribute("stroke", "black");
  path.setAttribute("stroke-width", "0.8");

  svg.appendChild(path);

}

function clearPlot() {

  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }

}

function drawRadial(method, region) {

  clearPlot();

  const meta = CID_DATA.metadata;

  const angles = meta.cid_sector_angles;

  const gwls = meta.gwls;

  const data =
    CID_DATA.data[method][region];

  const nRings = gwls.length;

  const ringSize = radius / nRings;

  for (const cid in data) {

    const fills = data[cid].fills;

    const angle1 = angles[cid][0];
    const angle2 = angles[cid][1];

    for (let i = 0; i < fills.length; i++) {

      const rOuter =
        radius - i * ringSize;

      const rInner =
        radius - (i + 1) * ringSize;

      drawSector(
        rOuter,
        rInner,
        angle1,
        angle2,
        fills[i]
      );

    }

  }

}

function updatePlot() {

  const method =
    document.getElementById("cid-method").value;

  const region =
    document.getElementById("cid-region").value;

  drawRadial(method, region);

}

fetch("/images/cid_data.json")
  .then(r => r.json())
  .then(data => {

    CID_DATA = data;

    document
      .getElementById("cid-method")
      .addEventListener(
        "change",
        updatePlot
      );

    document
      .getElementById("cid-region")
      .addEventListener(
        "change",
        updatePlot
      );

    updatePlot();

  });
