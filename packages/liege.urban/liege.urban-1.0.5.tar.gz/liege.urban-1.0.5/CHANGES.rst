Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.0.5 (2024-10-17)
------------------

New features:


- Compatible with imio.pm.wsclient 2.x.
  [aduchene] (URB-3148)


1.0.4 (2024-10-01)
------------------

New features:


- Add form_composition field to the export in `activity_report.py`.
  [aduchene] (SUP-37960)


Bug fixes:


- Fix performance issue with `activity_report.py`.
  [aduchene] (URB-3102)


1.0.3 (2024-04-01)
------------------

New features:


- Add caduc workflow state
  [jchandelle,mpeeters] (URB-3007)
- Add frozen workflow state to article127, inspection and ticket
  [jchandelle] (URB-3023)


Bug fixes:


- Fix an issue with zope users on urban homepage
  [mpeeters] (URB-2956)


1.0.2 (2023-11-21)
------------------

Bug fixes:


- Ensure that every licence types can add `UrbanEventMayor` and `UrbanEventAcknowledgment`
  [mpeeters] (SUP-33677)


1.0.1 (2023-11-16)
------------------

- Fix template for worklocation [URB-2930]
  [mpeeters]


1.0.0 (2023-11-09)
------------------

- Add get_work_location method.
  [fngaha]

- Initial release.
  [sdelcourt]
