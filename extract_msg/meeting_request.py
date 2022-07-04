import datetime

from typing import List, Set

from .meeting_related import MeetingRelated
from .enums import BusyStatus, RecurCalendarType, MeetingObjectChange, MeetingType


class MeetingRequest(MeetingRelated):
    """
    Class for handling Meeting Request and Meeting Update objects.
    """

    @property
    def appointmentClassType(self) -> str:
        """
        Indicates the value of the PidTagMessageClass property of the Meeting
        object that is to be generated from the Meeting Request object. MUST
        start with "IPM.Appointment".
        """
        return self._ensureSetNamed('_appointmentClassType', '0024')

    @property
    def calendarType(self) -> RecurCalendarType:
        """
        The value of the CalendarType field from the PidLidAppointmentRecur
        property if the Meeting Request object represents a recurring series or
        an exception.
        """
        return self._ensureSetNamed('_calendarType', '001C', overrideClass = RecurCalendarType)

    @property
    def changeHighlight(self) -> Set[MeetingObjectChange]:
        """
        Soecifies a bit field that indicates how the Meeting object has been
        changed.

        Returns a set of flags.
        """
        return self._ensureSetNamed('_changeHighlight', '8204', overrideClass = MeetingObjectChange.fromBits)

    @property
    def forwardInstance(self) -> bool:
        """
        Indicates that the Meeting Request object represents an exception to a
        recurring series, and it was forwarded (even when forwarded by the
        organizer) rather than being an invitation sent by the organizer.
        """
        return self._ensureSetNamed('_forwardInstance', '820A')

    @property
    def headerFormatProperties(self) -> constants.HEADER_FORMAT_TYPE:
        """
        Returns a dictionary of properties, in order, to be formatted into the
        header. Keys are the names to use in the header while the values are one
        of the following:
        None: Signifies no data was found for the property and it should be
            omitted from the header.
        str: A string to be formatted into the header using the string encoding.
        Tuple[Union[str, None], bool]: A string should be formatted into the
            header. If the bool is True, then place an empty string if the value
            is None, otherwise follow the same behavior as regular None.

        Additional note: If the value is an empty string, it will be dropped as
        well by default.
        """
        meetingOrganizerString = {
            ResponseStatus.NONE: None,
            ResponseStatus.ORGANIZED: 'Meeting organizer',
            ResponseStatus.TENTATIVE: 'Tentatively accepted',
            ResponseStatus.ACCEPTED: 'Accepted',
            ResponseStatus.DECLINED: 'Declined',
            ResponseStatus.NOT_RESPONDED: 'Not yet responded',
        }

        # Get the recurrence string.
        recur = '(none)'
        if self.appointmentRecur:
            recur = {
                RecurPatternType.DAY: 'Daily',
                RecurPatternType.WEEK: 'Weekly',
                RecurPatternType.MONTH: 'Monthly',
                RecurPatternType.MONTH_NTH: 'Monthly',
                RecurPatternType.MONTH_END: 'Monthly',
                RecurPatternType.HJ_MONTH: 'Monthly',
                RecurPatternType.HJ_MONTH_NTH: 'Monthly',
                RecurPatternType.HJ_MONTH_END: 'Monthly',
            }[self.appointmentRecur.patternType]

        showTime = None if self.appointmentNotAllowPropose else 'Tentative'

        return {
            '-main info-': {
                'Subject': self.subject,
                'Location': self.location,
            },
            '-date-': {
                'Start': self.startDate,
                'End': self.endDate,
                'Show Time As': showTime,
            },
            '-recurrence-': {
                'Recurrance': recur,
                'Recurrence Pattern': self.recurrencePattern,
            },
            '-status-': {
                'Meeting Status': meetingOrganizerString,
            },
            '-attendees-': {
                'Organizer': self.organizer,
                'Required Attendees': self.requiredAttendees,
                'Optional Attendees': self.optionalAttendees,
            },
            '-resources-': {
                'Resources':
            }
        }


    @property
    def intendedBusyStatus(self) -> BusyStatus:
        """
        The value of the busyStatus on the Meeting object in the organizer's
        calendar at the time the Meeting Request object or Meeting Update object
        was sent.
        """
        return self._ensureSetNamed('_intendedBusyStatus', '8224', overrideClass = BusyStatus)

    @property
    def meetingType(self) -> MeetingType:
        """
        The type of Meeting Request object or Meeting UpdateObject.
        """
        return self._ensureSetNamed('meetingType', '0026', overrideClass = MeetingType)

    @property
    def oldLocation(self) -> str:
        """
        The original value of the location property before a meeting update.
        """
        return self._ensureSetNamed('_oldLocation', '0028')

    @property
    def oldWhenEndWhole(self) -> datetime.datetime:
        """
        The original value of the appointmentEndWhole property before a meeting
        update.
        """
        return self._ensureSetNamed('_oldWhenEndWhole', '002A')

    @property
    def oldWhenStartWhole(self) -> datetime.datetime:
        """
        The original value of the appointmentStartWhole property before a
        meeting update.
        """
        return self._ensureSetNamed('_oldWhenStartWhole', '0029')
