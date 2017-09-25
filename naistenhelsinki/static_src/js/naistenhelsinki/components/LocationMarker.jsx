import React from 'react';
import PropTypes from 'prop-types';
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';


function getIcon(content) {
  return L.divIcon({
    className: "number-icon",
    iconSize: [22, 22],
    iconAnchor: [11, 11], // Position offset by half of the width and height
    popupAnchor: [0, -5],
    html: content
  });
}


export default function LocationMarker(props) {
  const { name, description, coordinates, iconNumber } = props;

  const icon = getIcon(iconNumber);

  return (
    <Marker key={name} position={coordinates.reverse()} icon={icon}>
      <Popup>
        <div dangerouslySetInnerHTML={{ __html: description }}/>
      </Popup>
    </Marker>
  );
}


LocationMarker.propTypes = {
  name: PropTypes.string,
  description: PropTypes.string,
  coordinates: PropTypes.array,
  iconNumber: PropTypes.number,
};
