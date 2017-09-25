import React, { Component } from 'react';
import { Map as LeafletMap, TileLayer } from 'react-leaflet';

import LocationMarker from './LocationMarker.jsx';


export default class Map extends Component {
  constructor(props) {
    super(props);
    this.position = [60.172059, 24.945831]; // Default to Helsinki's center
    this.bounds = [
      [59.9, 24.59],  // SouthWest corner
      [60.43, 25.3]  // NorthEast corner
    ];
  }

  getMarkers() {
    const places = this.props.places;

    return places.features.map((feature, index) => {
      if (!feature.geometry) return null;

      const iconNumber = index + 1;

      return (
        <LocationMarker
          key={index}
          name={feature.properties.name}
          description={feature.properties.description}
          coordinates={feature.geometry.coordinates}
          iconNumber={iconNumber}
        />
      );
    });
  }

  render() {
    if (!this.props.places) return null;

    const markers = this.getMarkers();

    return (
      <LeafletMap center={this.position} zoom={13}>
        <TileLayer
          url='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          minZoom={10} maxZoom={16} zoomControl={true}
        />
        {markers}
      </LeafletMap>
    );
  }
}
