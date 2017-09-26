import React from 'react';
import PropTypes from 'prop-types';
import { Marker } from 'react-leaflet';
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
  const { placeFeature, iconNumber, onClick } = props;

  const icon = getIcon(iconNumber);
  const position = placeFeature.geometry.coordinates.reverse();

  return (
    <Marker
      position={position}
      icon={icon}
      onClick={onClick}
    />
  );
}


LocationMarker.propTypes = {
  placeFeature: PropTypes.object,
  iconNumber: PropTypes.number,
  onClick: PropTypes.func,
};
