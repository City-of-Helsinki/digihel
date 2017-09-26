import React, { Component } from 'react';
import { Map as LeafletMap, TileLayer } from 'react-leaflet';

import PlaceModal from './PlaceModal.jsx';
import LocationMarker from './LocationMarker.jsx';


export default class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedPlace: null,
    };
    this.position = [60.172059, 24.945831]; // Center of Helsinki
    this.bounds = [
      [59.9, 24.59],  // SouthWest corner
      [60.43, 25.3],  // NorthEast corner
    ];
  }

  onDeselectPlace() {
    this.setState({
      selectedPlace: null,
    });
  }

  onSelectPlace(placeFeature) {
    this.setState({
      selectedPlace: placeFeature,
    });
  }

  getMarkers() {
    const places = this.props.places;

    return places.features.map((placeFeature, index) => {
      if (!placeFeature.geometry) return null;

      const iconNumber = index + 1;

      return (
        <LocationMarker
          key={placeFeature.properties.pk}
          placeFeature={placeFeature}
          iconNumber={iconNumber}
          onClick={() => this.onSelectPlace(placeFeature)}
        />
      );
    });
  }

  getModal() {
    if (!this.state.selectedPlace) return null;

    return (
      <PlaceModal
        placeFeature={this.state.selectedPlace}
        closeModal={() => this.onDeselectPlace()}
      />
    );
  }

  render() {
    if (!this.props.places) return null;

    return (
      <div>
        <LeafletMap center={this.position} zoom={13}>
          <TileLayer
            url='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            minZoom={10} maxZoom={16} zoomControl={true}
          />
          {this.getMarkers()}
        </LeafletMap>
        {this.getModal()}
      </div>
    );
  }
}
