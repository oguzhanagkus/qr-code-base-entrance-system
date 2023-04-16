import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

import '../flutter_flow/flutter_flow_theme.dart';

class LocationItemWidget extends StatefulWidget {
  const LocationItemWidget({
    Key key,
    this.locationName,
  }) : super(key: key);

  final String locationName;

  @override
  _LocationItemWidgetState createState() => _LocationItemWidgetState();
}

class _LocationItemWidgetState extends State<LocationItemWidget> {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsetsDirectional.fromSTEB(0, 0, 0, 10),
      child: Container(
        width: double.infinity,
        height: 60,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: FlutterFlowTheme.tertiaryColor,
            width: 0,
          ),
        ),
        alignment: AlignmentDirectional(0, 0),
        child: Padding(
          padding: EdgeInsetsDirectional.fromSTEB(20, 0, 20, 0),
          child: Row(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Padding(
                padding: EdgeInsetsDirectional.fromSTEB(0, 0, 10, 0),
                child: FaIcon(
                  FontAwesomeIcons.mapMarkerAlt,
                  color: FlutterFlowTheme.primary,
                  size: 20,
                ),
              ),
              Text(
                widget.locationName,
                style: FlutterFlowTheme.subtitle1.override(
                  fontFamily: 'Poppins',
                  color: FlutterFlowTheme.primaryColor,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
