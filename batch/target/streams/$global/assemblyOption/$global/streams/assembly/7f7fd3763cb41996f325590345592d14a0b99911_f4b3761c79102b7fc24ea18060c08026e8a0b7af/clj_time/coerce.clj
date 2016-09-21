(ns clj-time.coerce
  "Utilites to coerce Joda DateTime instances to and from various other types.
   For example, to convert a Joda DateTime to and from a Java long:

     => (to-long (date-time 1998 4 25))
     893462400000

     => (from-long 893462400000)
     #<DateTime 1998-04-25T00:00:00.000Z>"
  (:refer-clojure :exclude [extend])
  (:use clj-time.core)
  (:require [clj-time.format :as time-fmt])
  (:import (org.joda.time DateTime DateTimeZone))
  (:import java.util.Date java.sql.Timestamp))

(defprotocol ICoerce
  (#^org.joda.time.DateTime
    to-date-time [obj] "Convert `obj` to a Joda DateTime instance."))

(defn from-long
  "Returns a DateTime instance in the UTC time zone corresponding to the given
   number of milliseconds after the Unix epoch."
  [#^Long millis]
  (DateTime. millis #^DateTimeZone utc))

(defn from-string
  "return DateTime instance from string using
   formatters in clj-time.format, returning first
   which parses"
  [s]
  (first
   (for [f (vals time-fmt/formatters)
         :let [d (try (time-fmt/parse f s) (catch Exception _ nil))]
         :when d] d)))

(defn from-date
  "Returns a DateTime instance in the UTC time zone corresponding to the given
   Java Date object."
  [#^Date date]
  (from-long (.getTime date)))

(defn from-sql-date
  "Returns a DateTime instance in the UTC time zone corresponding to the given
   java.sql.Date object."
  [#^java.sql.Date sql-date]
  (from-long (.getTime sql-date)))

(defn to-long
  "Convert `obj` to the number of milliseconds after the Unix epoch."
  [obj]
  (if-let [dt (to-date-time obj)]
    (.getMillis dt)))

(defn to-date
  "Convert `obj` to a Java Date instance."
  [obj]
  (if-let [dt (to-date-time obj)]
    (Date. (.getMillis dt))))

(defn to-sql-date
  "Convert `obj` to a java.sql.Date instance."
  [obj]
  (if-let [dt (to-date-time obj)]
    (java.sql.Date. (.getMillis dt))))

(defn to-string
  "Returns a string representation of obj in UTC time-zone
  using (ISODateTimeFormat/dateTime) date-time representation."
  [obj]
  (if-let [#^DateTime dt (to-date-time obj)]
    (time-fmt/unparse (:date-time time-fmt/formatters) dt)))

(defn to-timestamp
  "Convert `obj` to a Java SQL Timestamp instance."
  [obj]
  (if-let [dt (to-date-time obj)]
    (Timestamp. (.getMillis dt))))

(extend-protocol ICoerce
  nil
  (to-date-time [_]
    nil)

  Date
  (to-date-time [date]
    (from-date date))

  java.sql.Date
  (to-date-time [sql-date]
    (from-sql-date sql-date))

  DateTime
  (to-date-time [date-time]
    date-time)

  Integer
  (to-date-time [integer]
    (from-long (long integer)))

  Long
  (to-date-time [long]
    (from-long long))

  String
  (to-date-time [string]
    (from-string string))

  Timestamp
  (to-date-time [timestamp]
    (from-date timestamp)))

