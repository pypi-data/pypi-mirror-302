# Generated from antlr/FriendlyDate.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .FriendlyDateParser import FriendlyDateParser
else:
    from FriendlyDateParser import FriendlyDateParser

# This class defines a complete generic visitor for a parse tree produced by FriendlyDateParser.

class FriendlyDateVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FriendlyDateParser#friendlyDateTime.
    def visitFriendlyDateTime(self, ctx:FriendlyDateParser.FriendlyDateTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateTime.
    def visitDateTime(self, ctx:FriendlyDateParser.DateTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#now.
    def visitNow(self, ctx:FriendlyDateParser.NowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#anyTz.
    def visitAnyTz(self, ctx:FriendlyDateParser.AnyTzContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#tz.
    def visitTz(self, ctx:FriendlyDateParser.TzContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#tzAbbreviation.
    def visitTzAbbreviation(self, ctx:FriendlyDateParser.TzAbbreviationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#friendlyDate.
    def visitFriendlyDate(self, ctx:FriendlyDateParser.FriendlyDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateAlone.
    def visitDateAlone(self, ctx:FriendlyDateParser.DateAloneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#before.
    def visitBefore(self, ctx:FriendlyDateParser.BeforeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#after.
    def visitAfter(self, ctx:FriendlyDateParser.AfterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#ago.
    def visitAgo(self, ctx:FriendlyDateParser.AgoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#time.
    def visitTime(self, ctx:FriendlyDateParser.TimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#midnight.
    def visitMidnight(self, ctx:FriendlyDateParser.MidnightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#noon.
    def visitNoon(self, ctx:FriendlyDateParser.NoonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateDelta.
    def visitDateDelta(self, ctx:FriendlyDateParser.DateDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateTimeDelta.
    def visitDateTimeDelta(self, ctx:FriendlyDateParser.DateTimeDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#yearsDelta.
    def visitYearsDelta(self, ctx:FriendlyDateParser.YearsDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#monthsDelta.
    def visitMonthsDelta(self, ctx:FriendlyDateParser.MonthsDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#weeksDelta.
    def visitWeeksDelta(self, ctx:FriendlyDateParser.WeeksDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#daysDelta.
    def visitDaysDelta(self, ctx:FriendlyDateParser.DaysDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#hoursDelta.
    def visitHoursDelta(self, ctx:FriendlyDateParser.HoursDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#minutesDelta.
    def visitMinutesDelta(self, ctx:FriendlyDateParser.MinutesDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#secondsDelta.
    def visitSecondsDelta(self, ctx:FriendlyDateParser.SecondsDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#timeAbsolute.
    def visitTimeAbsolute(self, ctx:FriendlyDateParser.TimeAbsoluteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#hour.
    def visitHour(self, ctx:FriendlyDateParser.HourContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#minute.
    def visitMinute(self, ctx:FriendlyDateParser.MinuteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#second.
    def visitSecond(self, ctx:FriendlyDateParser.SecondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#twoDigitFloatNumber.
    def visitTwoDigitFloatNumber(self, ctx:FriendlyDateParser.TwoDigitFloatNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#amPm.
    def visitAmPm(self, ctx:FriendlyDateParser.AmPmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#am.
    def visitAm(self, ctx:FriendlyDateParser.AmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#pm.
    def visitPm(self, ctx:FriendlyDateParser.PmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#date.
    def visitDate(self, ctx:FriendlyDateParser.DateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeByDate.
    def visitDateRelativeByDate(self, ctx:FriendlyDateParser.DateRelativeByDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelative.
    def visitDateRelative(self, ctx:FriendlyDateParser.DateRelativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#today.
    def visitToday(self, ctx:FriendlyDateParser.TodayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#yesterday.
    def visitYesterday(self, ctx:FriendlyDateParser.YesterdayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#tomorrow.
    def visitTomorrow(self, ctx:FriendlyDateParser.TomorrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#theDayBeforeYesterday.
    def visitTheDayBeforeYesterday(self, ctx:FriendlyDateParser.TheDayBeforeYesterdayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#theDayAfterTomorrow.
    def visitTheDayAfterTomorrow(self, ctx:FriendlyDateParser.TheDayAfterTomorrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeDay.
    def visitDateRelativeDay(self, ctx:FriendlyDateParser.DateRelativeDayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeWeek.
    def visitDateRelativeWeek(self, ctx:FriendlyDateParser.DateRelativeWeekContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeMonth.
    def visitDateRelativeMonth(self, ctx:FriendlyDateParser.DateRelativeMonthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeYearWithMonth.
    def visitDateRelativeYearWithMonth(self, ctx:FriendlyDateParser.DateRelativeYearWithMonthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeYearWithoutMonth.
    def visitDateRelativeYearWithoutMonth(self, ctx:FriendlyDateParser.DateRelativeYearWithoutMonthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeMonthWeek.
    def visitDateRelativeMonthWeek(self, ctx:FriendlyDateParser.DateRelativeMonthWeekContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeYearWeek.
    def visitDateRelativeYearWeek(self, ctx:FriendlyDateParser.DateRelativeYearWeekContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeMonthDayPosition.
    def visitDateRelativeMonthDayPosition(self, ctx:FriendlyDateParser.DateRelativeMonthDayPositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateRelativeYearDayPosition.
    def visitDateRelativeYearDayPosition(self, ctx:FriendlyDateParser.DateRelativeYearDayPositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#lastR.
    def visitLastR(self, ctx:FriendlyDateParser.LastRContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#nextR.
    def visitNextR(self, ctx:FriendlyDateParser.NextRContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#thisR.
    def visitThisR(self, ctx:FriendlyDateParser.ThisRContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#last.
    def visitLast(self, ctx:FriendlyDateParser.LastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateAbsolute.
    def visitDateAbsolute(self, ctx:FriendlyDateParser.DateAbsoluteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateMonthAsName.
    def visitDateMonthAsName(self, ctx:FriendlyDateParser.DateMonthAsNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#lastDay.
    def visitLastDay(self, ctx:FriendlyDateParser.LastDayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateMonthAsNumber.
    def visitDateMonthAsNumber(self, ctx:FriendlyDateParser.DateMonthAsNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateWithWeek.
    def visitDateWithWeek(self, ctx:FriendlyDateParser.DateWithWeekContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateWithDayPosition.
    def visitDateWithDayPosition(self, ctx:FriendlyDateParser.DateWithDayPositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#weekDayPositionOrdinal.
    def visitWeekDayPositionOrdinal(self, ctx:FriendlyDateParser.WeekDayPositionOrdinalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#weekDayPositionLast.
    def visitWeekDayPositionLast(self, ctx:FriendlyDateParser.WeekDayPositionLastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dayPositionNumber.
    def visitDayPositionNumber(self, ctx:FriendlyDateParser.DayPositionNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dayPositionOrdinal.
    def visitDayPositionOrdinal(self, ctx:FriendlyDateParser.DayPositionOrdinalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#lastWeek.
    def visitLastWeek(self, ctx:FriendlyDateParser.LastWeekContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#weekNumber.
    def visitWeekNumber(self, ctx:FriendlyDateParser.WeekNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#twoDigitNumberLeft.
    def visitTwoDigitNumberLeft(self, ctx:FriendlyDateParser.TwoDigitNumberLeftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#twoDigitNumberRight.
    def visitTwoDigitNumberRight(self, ctx:FriendlyDateParser.TwoDigitNumberRightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateLongNumber.
    def visitDateLongNumber(self, ctx:FriendlyDateParser.DateLongNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dateYear.
    def visitDateYear(self, ctx:FriendlyDateParser.DateYearContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#monthAsNameOrNumber.
    def visitMonthAsNameOrNumber(self, ctx:FriendlyDateParser.MonthAsNameOrNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#monthAsName.
    def visitMonthAsName(self, ctx:FriendlyDateParser.MonthAsNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dayAsNumberOrOrdinal.
    def visitDayAsNumberOrOrdinal(self, ctx:FriendlyDateParser.DayAsNumberOrOrdinalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dayAsOrdinal.
    def visitDayAsOrdinal(self, ctx:FriendlyDateParser.DayAsOrdinalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#anyOrdinal.
    def visitAnyOrdinal(self, ctx:FriendlyDateParser.AnyOrdinalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#twoDigitOrdinal.
    def visitTwoDigitOrdinal(self, ctx:FriendlyDateParser.TwoDigitOrdinalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#wordOrdinal.
    def visitWordOrdinal(self, ctx:FriendlyDateParser.WordOrdinalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#monthAsNumber.
    def visitMonthAsNumber(self, ctx:FriendlyDateParser.MonthAsNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#dayAsNumber.
    def visitDayAsNumber(self, ctx:FriendlyDateParser.DayAsNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#yearLong.
    def visitYearLong(self, ctx:FriendlyDateParser.YearLongContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#fourDigitNumber.
    def visitFourDigitNumber(self, ctx:FriendlyDateParser.FourDigitNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#twoDigitNumber.
    def visitTwoDigitNumber(self, ctx:FriendlyDateParser.TwoDigitNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#zNumber.
    def visitZNumber(self, ctx:FriendlyDateParser.ZNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#qNumber.
    def visitQNumber(self, ctx:FriendlyDateParser.QNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#anyFloatNumber.
    def visitAnyFloatNumber(self, ctx:FriendlyDateParser.AnyFloatNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#anyDigitNumber.
    def visitAnyDigitNumber(self, ctx:FriendlyDateParser.AnyDigitNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#weekDay.
    def visitWeekDay(self, ctx:FriendlyDateParser.WeekDayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FriendlyDateParser#separator.
    def visitSeparator(self, ctx:FriendlyDateParser.SeparatorContext):
        return self.visitChildren(ctx)



del FriendlyDateParser