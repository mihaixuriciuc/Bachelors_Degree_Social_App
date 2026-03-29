import { Fragment } from "react/jsx-runtime";
import { MouseEvent, useState } from "react";

function ListGroup() {
  const cities = [
    "Bogdanesti",
    "Pitesti",
    "Ploiesti",
    "Onesti",
    "Voinesti",
    "Pildesti",
    "Stroiesti",
    "Ilisesti",
    "Tiganesti",
    "Costinesti",
  ];

  //HOok
  const [selectedIndex, setSelectedIndex] = useState(-1);

  let convertedCities = cities.map((city, index) => (
    <li
      className={
        selectedIndex === index ? "list-group-item active" : "list-group-item"
      }
      key={city}
      onClick={() => setSelectedIndex(index)}
    >
      {city}
    </li>
  ));

  return (
    <>
      <h1>Cities</h1>{" "}
      <ul className="list-group">
        {" "}
        {convertedCities.length === 0 && (
          <li className="list-group-item">No cities in the list</li>
        )}
        {convertedCities}
      </ul>
    </>
  );
}

export default ListGroup;
