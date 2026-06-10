import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:mobile/src/app/sync_p_app.dart';

void main() {
  testWidgets('searches places and opens details', (WidgetTester tester) async {
    await tester.pumpWidget(const SyncPApp());
    await tester.pump();

    expect(find.text('Discover places'), findsOneWidget);
    expect(find.text('Buna Bistro'), findsOneWidget);
    expect(find.text('Unity Park'), findsOneWidget);

    await tester.enterText(find.byType(TextField), 'park');
    await tester.pump();
    await tester.pump();

    expect(find.text('Unity Park'), findsOneWidget);
    expect(find.text('Friendship Park'), findsOneWidget);
    expect(find.text('Buna Bistro'), findsNothing);

    await tester.tap(find.text('Unity Park'));
    await tester.pumpAndSettle();

    expect(find.text('Menelik II Avenue, Addis Ababa'), findsOneWidget);
    expect(find.text('Open in Google Maps'), findsOneWidget);
  });
}
