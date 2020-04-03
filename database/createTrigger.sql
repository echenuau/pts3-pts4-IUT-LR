CREATE OR REPLACE FUNCTION qgis_trigger()
RETURNS trigger
AS $qgis$
BEGIN
	NEW.location_point := ST_SetSRID(ST_MakePoint(NEW.coordinates[0],NEW.coordinates[1]),4326);
	IF NEW.vector_robot_direction IS NOT NULL THEN
		NEW.robot_direction := ST_SetSRID(ST_MakeLine(ST_MakePoint(NEW.coordinates[0],NEW.coordinates[1]), ST_MakePoint(NEW.coordinates[0]+NEW.vector_robot_direction[0],NEW.coordinates[1]+NEW.vector_robot_direction[1])),4326);
	END IF;
  	RETURN NEW;
END;
$qgis$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS qgis_trigger on "public"."qgis";

CREATE TRIGGER qgis_trigger BEFORE INSERT OR UPDATE ON qgis
	FOR EACH ROW EXECUTE PROCEDURE qgis_trigger();