import React, { Component } from 'react';
import Modal from 'react-modal';


export default class PlaceModal extends Component {
  getImage() {
    const imageUrl = this.props.placeFeature.properties.image_url;
    if (!imageUrl) return null;

    return (
      <div className="nh-modal-image">
        <img src={imageUrl}/>
      </div>
    );
  }

  render() {
    const placeFeature = this.props.placeFeature;

    return (
      <Modal
        isOpen
        style={this.customStyles}
        onRequestClose={this.props.closeModal}
        shouldCloseOnOverlayClick={true}
        contentLabel="Place modal"
      >
        <div className="nh-modal-header">
          <button className="btn btn-default close-modal" onClick={this.props.closeModal}>
            &times;
          </button>
          <h1>{placeFeature.properties.modal_title}</h1>
        </div>
        {this.getImage()}
        <div
          className="nh-modal-content"
          dangerouslySetInnerHTML={{ __html: placeFeature.properties.description }}
        />
      </Modal>
    );
  }
}
