from django.contrib.gis.serializers.geojson import Serializer as GeoJsonSerializer


class PlaceSerializer(GeoJsonSerializer):
    """
    A GeoJson serializer that can serialize property function values.
    """

    def serialize_property(self, obj):
        model = type(obj)
        for field in self.selected_fields:
            if hasattr(model, field) and type(getattr(model, field)) == property:
                self.handle_property(obj, field)

    def handle_property(self, obj, field):
        self._current[field] = getattr(obj, field)

    def end_object(self, obj):
        self.serialize_property(obj)
        super(GeoJsonSerializer, self).end_object(obj)
