import '../domain/entities/place.dart';

const samplePlaces = <Place>[
  Place(
    id: 'buna-bistro',
    name: 'Buna Bistro',
    category: PlaceCategory.cafe,
    address: 'Bole Road, Addis Ababa',
    latitude: 9.005401,
    longitude: 38.763611,
  ),
  Place(
    id: 'tomoca-coffee',
    name: 'Tomoca Coffee',
    category: PlaceCategory.cafe,
    address: 'Wawel Street, Addis Ababa',
    latitude: 9.033140,
    longitude: 38.750080,
  ),
  Place(
    id: 'kategna-restaurant',
    name: 'Kategna Restaurant',
    category: PlaceCategory.restaurant,
    address: 'Kazanchis, Addis Ababa',
    latitude: 9.020920,
    longitude: 38.761420,
  ),
  Place(
    id: 'unity-park',
    name: 'Unity Park',
    category: PlaceCategory.park,
    address: 'Menelik II Avenue, Addis Ababa',
    latitude: 9.030100,
    longitude: 38.761300,
  ),
  Place(
    id: 'friendship-park',
    name: 'Friendship Park',
    category: PlaceCategory.park,
    address: 'African Union Street, Addis Ababa',
    latitude: 9.014870,
    longitude: 38.758120,
  ),
  Place(
    id: 'sishu-burger',
    name: 'Sishu Burger',
    category: PlaceCategory.restaurant,
    address: 'Old Airport, Addis Ababa',
    latitude: 8.994090,
    longitude: 38.733410,
  ),
];
