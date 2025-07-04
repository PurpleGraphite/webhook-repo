import { parseISO } from 'date-fns';
import { formatInTimeZone } from 'date-fns-tz';

function convertTimestamp(isoString: string) {
	const date = parseISO(isoString);
	return formatInTimeZone(
		date,
		'UTC',
		"do MMMM yyyy - hh:mm a 'UTC'"
	);
}

export default convertTimestamp;
