-- -----------------------------------------------------------------------|
-- Script d'initialisation du site éditorial minimum de l'AppStore Lutece |
-- -----------------------------------------------------------------------|

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


DROP DATABASE IF EXISTS `site-edito-mini`;
CREATE DATABASE IF NOT EXISTS `site-edito-mini` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

CREATE USER 'lutece'@'%' IDENTIFIED BY 'demo';
GRANT ALL PRIVILEGES ON `site-edito-mini`.* TO 'lutece'@'%';
USE `site-edito-mini`;


-- Dumping structure for table site-edito-mini.childpages_portlet
DROP TABLE IF EXISTS `childpages_portlet`;
CREATE TABLE IF NOT EXISTS `childpages_portlet` (
  `id_portlet` int(11) NOT NULL DEFAULT '0',
  `id_child_page` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_portlet`,`id_child_page`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.childpages_portlet: 5 rows
/*!40000 ALTER TABLE `childpages_portlet` DISABLE KEYS */;
INSERT INTO `childpages_portlet` (`id_portlet`, `id_child_page`) VALUES
	(83, 1),
	(85, 1),
	(87, 3),
	(88, 1),
	(89, 1);
/*!40000 ALTER TABLE `childpages_portlet` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.contact
DROP TABLE IF EXISTS `contact`;
CREATE TABLE IF NOT EXISTS `contact` (
  `id_contact` int(11) NOT NULL DEFAULT '0',
  `description` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `email` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `workgroup_key` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'all',
  `hits` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_contact`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.contact: 2 rows
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` (`id_contact`, `description`, `email`, `workgroup_key`, `hits`) VALUES
	(1, 'Contact 1', 'adresse_email_du_contact_1@domaine.com', 'all', 0),
	(2, 'Contact 2', 'adresse_email_du_contact_2@domaine.com', 'all', 0);
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.contact_list
DROP TABLE IF EXISTS `contact_list`;
CREATE TABLE IF NOT EXISTS `contact_list` (
  `id_contact_list` int(11) NOT NULL DEFAULT '0',
  `label_contact_list` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `description_contact_list` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `workgroup_key` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'all',
  `role` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'none',
  `contact_list_order` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_contact_list`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.contact_list: 1 rows
/*!40000 ALTER TABLE `contact_list` DISABLE KEYS */;
INSERT INTO `contact_list` (`id_contact_list`, `label_contact_list`, `description_contact_list`, `workgroup_key`, `role`, `contact_list_order`) VALUES
	(1, 'Liste de contacts', 'Ceci est une liste de contacts', 'all', 'none', 1);
/*!40000 ALTER TABLE `contact_list` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.contact_list_contact
DROP TABLE IF EXISTS `contact_list_contact`;
CREATE TABLE IF NOT EXISTS `contact_list_contact` (
  `id_contact_list` int(11) NOT NULL DEFAULT '0',
  `id_contact` int(11) NOT NULL DEFAULT '0',
  `contact_order` int(11) NOT NULL DEFAULT '0',
  `hits` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_contact_list`,`id_contact`,`contact_order`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.contact_list_contact: 2 rows
/*!40000 ALTER TABLE `contact_list_contact` DISABLE KEYS */;
INSERT INTO `contact_list_contact` (`id_contact_list`, `id_contact`, `contact_order`, `hits`) VALUES
	(1, 1, 1, 0),
	(1, 2, 2, 0);
/*!40000 ALTER TABLE `contact_list_contact` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_dashboard
DROP TABLE IF EXISTS `core_admin_dashboard`;
CREATE TABLE IF NOT EXISTS `core_admin_dashboard` (
  `dashboard_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `dashboard_column` int(11) NOT NULL,
  `dashboard_order` int(11) NOT NULL,
  PRIMARY KEY (`dashboard_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_dashboard: 2 rows
/*!40000 ALTER TABLE `core_admin_dashboard` DISABLE KEYS */;
INSERT INTO `core_admin_dashboard` (`dashboard_name`, `dashboard_column`, `dashboard_order`) VALUES
	('usersAdminDashboardComponent', 1, 1),
	('searchAdminDashboardComponent', 1, 2);
/*!40000 ALTER TABLE `core_admin_dashboard` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_mailinglist
DROP TABLE IF EXISTS `core_admin_mailinglist`;
CREATE TABLE IF NOT EXISTS `core_admin_mailinglist` (
  `id_mailinglist` int(11) NOT NULL DEFAULT '0',
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `workgroup` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id_mailinglist`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_mailinglist: 1 rows
/*!40000 ALTER TABLE `core_admin_mailinglist` DISABLE KEYS */;
INSERT INTO `core_admin_mailinglist` (`id_mailinglist`, `name`, `description`, `workgroup`) VALUES
	(1, 'admin', 'admin', 'all');
/*!40000 ALTER TABLE `core_admin_mailinglist` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_mailinglist_filter
DROP TABLE IF EXISTS `core_admin_mailinglist_filter`;
CREATE TABLE IF NOT EXISTS `core_admin_mailinglist_filter` (
  `id_mailinglist` int(11) NOT NULL DEFAULT '0',
  `workgroup` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `role` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id_mailinglist`,`workgroup`,`role`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_mailinglist_filter: 1 rows
/*!40000 ALTER TABLE `core_admin_mailinglist_filter` DISABLE KEYS */;
INSERT INTO `core_admin_mailinglist_filter` (`id_mailinglist`, `workgroup`, `role`) VALUES
	(1, 'all', 'super_admin');
/*!40000 ALTER TABLE `core_admin_mailinglist_filter` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_right
DROP TABLE IF EXISTS `core_admin_right`;
CREATE TABLE IF NOT EXISTS `core_admin_right` (
  `id_right` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `level_right` smallint(6) DEFAULT NULL,
  `admin_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_updatable` int(11) NOT NULL DEFAULT '0',
  `plugin_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id_feature_group` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `icon_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `documentation_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id_order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_right`),
  KEY `index_right` (`level_right`,`admin_url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_right: 32 rows
/*!40000 ALTER TABLE `core_admin_right` DISABLE KEYS */;
INSERT INTO `core_admin_right` (`id_right`, `name`, `level_right`, `admin_url`, `description`, `is_updatable`, `plugin_name`, `id_feature_group`, `icon_url`, `documentation_url`, `id_order`) VALUES
	('CORE_ADMIN_SITE', 'portal.site.adminFeature.admin_site.name', 2, 'jsp/admin/site/AdminSite.jsp', 'portal.site.adminFeature.admin_site.description', 1, NULL, 'SITE', 'images/admin/skin/features/admin_site.png', 'jsp/admin/documentation/AdminDocumentation.jsp?doc=admin-site', 1),
	('CORE_CACHE_MANAGEMENT', 'portal.system.adminFeature.cache_management.name', 0, 'jsp/admin/system/ManageCaches.jsp', 'portal.system.adminFeature.cache_management.description', 1, '', 'SYSTEM', 'images/admin/skin/features/manage_caches.png', NULL, 1),
	('CORE_SEARCH_INDEXATION', 'portal.search.adminFeature.indexer.name', 0, 'jsp/admin/search/ManageSearchIndexation.jsp', 'portal.search.adminFeature.indexer.description', 0, '', 'SYSTEM', NULL, NULL, 2),
	('CORE_SEARCH_MANAGEMENT', 'portal.search.adminFeature.search_management.name', 0, 'jsp/admin/search/ManageSearch.jsp', 'portal.search.adminFeature.search_management.description', 0, '', 'SYSTEM', NULL, NULL, 3),
	('CORE_LOGS_VISUALISATION', 'portal.system.adminFeature.logs_visualisation.name', 0, 'jsp/admin/system/ManageFilesSystem.jsp', 'portal.system.adminFeature.logs_visualisation.description', 1, '', 'SYSTEM', 'images/admin/skin/features/view_logs.png', NULL, 4),
	('CORE_MODES_MANAGEMENT', 'portal.style.adminFeature.modes_management.name', 0, 'jsp/admin/style/ManageModes.jsp', 'portal.style.adminFeature.modes_management.description', 1, '', 'STYLE', 'images/admin/skin/features/manage_modes.png', NULL, 1),
	('CORE_PAGE_TEMPLATE_MANAGEMENT', 'portal.style.adminFeature.page_template_management.name', 0, 'jsp/admin/style/ManagePageTemplates.jsp', 'portal.style.adminFeature.page_template_management.description', 0, '', 'STYLE', 'images/admin/skin/features/manage_page_templates.png', NULL, 2),
	('CORE_PLUGINS_MANAGEMENT', 'portal.system.adminFeature.plugins_management.name', 0, 'jsp/admin/system/ManagePlugins.jsp', 'portal.system.adminFeature.plugins_management.description', 1, '', 'SYSTEM', 'images/admin/skin/features/manage_plugins.png', NULL, 5),
	('CORE_PROPERTIES_MANAGEMENT', 'portal.site.adminFeature.properties_management.name', 2, 'jsp/admin/ManageProperties.jsp', 'portal.site.adminFeature.properties_management.description', 0, NULL, 'SITE', NULL, 'jsp/admin/documentation/AdminDocumentation.jsp?doc=admin-properties', 2),
	('CORE_STYLESHEET_MANAGEMENT', 'portal.style.adminFeature.stylesheet_management.name', 0, 'jsp/admin/style/ManageStyleSheets.jsp', 'portal.style.adminFeature.stylesheet_management.description', 1, '', 'STYLE', 'images/admin/skin/features/manage_stylesheets.png', NULL, 3),
	('CORE_STYLES_MANAGEMENT', 'portal.style.adminFeature.styles_management.name', 0, 'jsp/admin/style/ManageStyles.jsp', 'portal.style.adminFeature.styles_management.description', 1, '', 'STYLE', 'images/admin/skin/features/manage_styles.png', NULL, 4),
	('CORE_USERS_MANAGEMENT', 'portal.users.adminFeature.users_management.name', 2, 'jsp/admin/user/ManageUsers.jsp', 'portal.users.adminFeature.users_management.description', 1, '', 'MANAGERS', 'images/admin/skin/features/manage_users.png', NULL, 1),
	('CORE_FEATURES_MANAGEMENT', 'portal.admin.adminFeature.features_management.name', 0, 'jsp/admin/features/ManageGroups.jsp', 'portal.admin.adminFeature.features_management.description', 0, '', 'SYSTEM', 'images/admin/skin/features/manage_features.png', NULL, 6),
	('CORE_RBAC_MANAGEMENT', 'portal.rbac.adminFeature.rbac_management.name', 0, 'jsp/admin/rbac/ManageRoles.jsp', 'portal.rbac.adminFeature.rbac_management.description', 0, '', 'MANAGERS', 'images/admin/skin/features/manage_rbac.png', NULL, 2),
	('CORE_DAEMONS_MANAGEMENT', 'portal.system.adminFeature.daemons_management.name', 0, 'jsp/admin/system/ManageDaemons.jsp', 'portal.system.adminFeature.daemons_management.description', 0, '', 'SYSTEM', NULL, NULL, 7),
	('CORE_WORKGROUPS_MANAGEMENT', 'portal.workgroup.adminFeature.workgroups_management.name', 2, 'jsp/admin/workgroup/ManageWorkgroups.jsp', 'portal.workgroup.adminFeature.workgroups_management.description', 0, '', 'MANAGERS', 'images/admin/skin/features/manage_workgroups.png', NULL, 3),
	('CORE_ROLES_MANAGEMENT', 'portal.role.adminFeature.roles_management.name', 2, 'jsp/admin/role/ManagePageRole.jsp', 'portal.role.adminFeature.roles_management.description', 0, NULL, 'USERS', 'images/admin/skin/features/manage_roles.png', NULL, 1),
	('CORE_MAILINGLISTS_MANAGEMENT', 'portal.mailinglist.adminFeature.mailinglists_management.name', 2, 'jsp/admin/mailinglist/ManageMailingLists.jsp', 'portal.mailinglist.adminFeature.mailinglists_management.description', 0, '', 'MANAGERS', 'images/admin/skin/features/manage_mailinglists.png', NULL, 4),
	('CORE_LEVEL_RIGHT_MANAGEMENT', 'portal.users.adminFeature.level_right_management.name', 2, 'jsp/admin/features/ManageLevels.jsp', 'portal.users.adminFeature.level_right_management.description', 0, '', 'MANAGERS', 'images/admin/skin/features/manage_rights_levels.png', NULL, 5),
	('CORE_LINK_SERVICE_MANAGEMENT', 'portal.insert.adminFeature.linkService_management.name', 2, NULL, 'portal.insert.adminFeature.linkService_management.description', 0, NULL, NULL, NULL, NULL, 1),
	('CORE_RIGHT_MANAGEMENT', 'portal.users.adminFeature.right_management.name', 0, 'jsp/admin/features/ManageRights.jsp', 'portal.users.adminFeature.right_management.description', 0, '', 'MANAGERS', 'images/admin/skin/features/manage_rights_levels.png', NULL, 6),
	('CORE_ADMINDASHBOARD_MANAGEMENT', 'portal.admindashboard.adminFeature.right_management.name', 0, 'jsp/admin/admindashboard/ManageAdminDashboards.jsp', 'portal.admindashboard.adminFeature.right_management.description', 0, '', 'SYSTEM', 'images/admin/skin/features/manage_admindashboards.png', NULL, 8),
	('CORE_DASHBOARD_MANAGEMENT', 'portal.dashboard.adminFeature.dashboard_management.name', 0, 'jsp/admin/dashboard/ManageDashboards.jsp', 'portal.dashboard.adminFeature.dashboard_management.description', 0, '', 'SYSTEM', 'images/admin/skin/features/manage_dashboards.png', NULL, 9),
	('CORE_XSL_EXPORT_MANAGEMENT', 'portal.xsl.adminFeature.xsl_export_management.name', 2, 'jsp/admin/xsl/ManageXslExport.jsp', 'portal.xsl.adminFeature.xsl_export_management.description', 1, '', 'SYSTEM', NULL, NULL, 11),
	('CORE_GLOBAL_MANAGEMENT', 'portal.globalmanagement.adminFeature.global_management.name', 2, 'jsp/admin/globalmanagement/GetGlobalManagement.jsp', 'portal.globalmanagement.adminFeature.global_management.description', 1, '', 'SYSTEM', NULL, NULL, 10),
	('CONTACT_MANAGEMENT', 'contact.adminFeature.contact_management.name', 3, 'jsp/admin/plugins/contact/ManageContactsHome.jsp', 'contact.adminFeature.contact_management.description', 0, 'contact', 'APPLICATIONS', NULL, NULL, 1),
	('RESOURCE_EXTENDER_MANAGEMENT', 'extend.adminFeature.resource_extenders_management.name', 2, 'jsp/admin/plugins/extend/ManageResourceExtendersByResource.jsp', 'extend.adminFeature.resource_extenders_management.description', 0, 'extend', 'SITE', NULL, 'jsp/admin/documentation/AdminDocumentation.jsp?doc=admin-extend', 5),
	('MANAGE_OPENGRAPH_SOCIALHUB', 'module.extend.opengraph.adminFeature.manage_opengraph_socialhub.name', 2, 'jsp/admin/plugins/extend/modules/opengraph/GetManageOpengraphSocialHub.jsp', 'module.extend.opengraph.adminFeature.manage_opengraph_socialhub.description', 0, 'extend-opengraph', 'SITE', NULL, 'jsp/admin/documentation/AdminDocumentation.jsp?doc=admin-extend-opengraph', 6),
	('SEARCH_STATS_MANAGEMENT', 'searchstats.adminFeature.searchstats_management.name', 1, 'jsp/admin/plugins/searchstats/ManageSearchStats.jsp', 'searchstats.adminFeature.searchstats_management.description', 0, 'searchstats', 'SITE', NULL, NULL, 4),
	('SEO_MANAGEMENT', 'seo.adminFeature.seo_management.name', 0, 'jsp/admin/plugins/seo/ManageSEO.jsp', 'seo.adminFeature.seo_management.description', 0, 'seo', 'SITE', NULL, NULL, 3),
	('SYSTEMINFO_MANAGEMENT', 'systeminfo.adminFeature.systeminfo_management.name', 0, 'jsp/admin/plugins/systeminfo/ManageSystemInfo.jsp', 'systeminfo.adminFeature.systeminfo_management.description', 0, 'systeminfo', 'SYSTEM', NULL, NULL, 12),
	('THEME_MANAGEMENT', 'theme.adminFeature.theme_management.name', 0, 'jsp/admin/plugins/theme/ManageThemes.jsp', 'theme.adminFeature.theme_management.description', 0, 'theme', 'STYLE', NULL, 'jsp/admin/documentation/AdminDocumentation.jsp?doc=admin-theme', 5);
/*!40000 ALTER TABLE `core_admin_right` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_role
DROP TABLE IF EXISTS `core_admin_role`;
CREATE TABLE IF NOT EXISTS `core_admin_role` (
  `role_key` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `role_description` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`role_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_role: 5 rows
/*!40000 ALTER TABLE `core_admin_role` DISABLE KEYS */;
INSERT INTO `core_admin_role` (`role_key`, `role_description`) VALUES
	('all_site_manager', 'Site Manager'),
	('super_admin', 'Super Administrateur'),
	('extend_manager', 'Gestion des type de ressource d\'extend'),
	('extend_opengraph_manager', 'Gestion des réseaux sociaux'),
	('theme_manager', 'Theme management');
/*!40000 ALTER TABLE `core_admin_role` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_role_resource
DROP TABLE IF EXISTS `core_admin_role_resource`;
CREATE TABLE IF NOT EXISTS `core_admin_role_resource` (
  `rbac_id` int(11) NOT NULL DEFAULT '0',
  `role_key` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `resource_type` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `resource_id` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `permission` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`rbac_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_role_resource: 11 rows
/*!40000 ALTER TABLE `core_admin_role_resource` DISABLE KEYS */;
INSERT INTO `core_admin_role_resource` (`rbac_id`, `role_key`, `resource_type`, `resource_id`, `permission`) VALUES
	(57, 'all_site_manager', 'PAGE', '*', 'VIEW'),
	(58, 'all_site_manager', 'PAGE', '*', 'MANAGE'),
	(77, 'super_admin', 'INSERT_SERVICE', '*', '*'),
	(101, 'all_site_manager', 'PORTLET_TYPE', '*', '*'),
	(111, 'all_site_manager', 'ADMIN_USER', '*', '*'),
	(137, 'all_site_manager', 'SEARCH_SERVICE', '*', '*'),
	(164, 'all_site_manager', 'XSL_EXPORT', '*', '*'),
	(990, 'extend_manager', 'EXTEND_EXTENDABLE_RESOURCE_TYPE', '*', '*'),
	(991, 'extend_manager', 'EXTEND_EXTENDABLE_RESOURCE', '*', '*'),
	(558, 'extend_opengraph_manager', 'OPENGRAPH_SOCIAL_HUB', '*', '*'),
	(155, 'theme_manager', 'THEME', '*', '*');
/*!40000 ALTER TABLE `core_admin_role_resource` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_user
DROP TABLE IF EXISTS `core_admin_user`;
CREATE TABLE IF NOT EXISTS `core_admin_user` (
  `id_user` int(11) NOT NULL DEFAULT '0',
  `access_code` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `last_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `first_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `email` varchar(256) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  `status` smallint(6) NOT NULL DEFAULT '0',
  `password` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `locale` varchar(10) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'fr',
  `level_user` smallint(6) NOT NULL DEFAULT '0',
  `reset_password` smallint(6) NOT NULL DEFAULT '0',
  `accessibility_mode` smallint(6) NOT NULL DEFAULT '0',
  `password_max_valid_date` timestamp NULL DEFAULT NULL,
  `account_max_valid_date` bigint(20) DEFAULT NULL,
  `nb_alerts_sent` int(11) NOT NULL DEFAULT '0',
  `last_login` timestamp NOT NULL DEFAULT '1980-01-01 00:00:00',
  PRIMARY KEY (`id_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_user: 4 rows
/*!40000 ALTER TABLE `core_admin_user` DISABLE KEYS */;
INSERT INTO `core_admin_user` (`id_user`, `access_code`, `last_name`, `first_name`, `email`, `status`, `password`, `locale`, `level_user`, `reset_password`, `accessibility_mode`, `password_max_valid_date`, `account_max_valid_date`, `nb_alerts_sent`, `last_login`) VALUES
	(1, 'admin', 'Admin', 'admin', 'admin@lutece.fr', 0, 'adminadmin', 'fr', 0, 0, 0, NULL, 1404914444402, 0, '2013-07-09 16:00:44'),
	(2, 'lutece', 'Lutèce', 'lutece', 'lutece@lutece.fr', 0, 'adminadmin', 'fr', 1, 0, 0, NULL, NULL, 0, '1980-01-01 00:00:00'),
	(3, 'redac', 'redac', 'redac', 'redac@lutece.fr', 0, 'adminadmin', 'fr', 2, 0, 0, NULL, NULL, 0, '1980-01-01 00:00:00'),
	(4, 'valid', 'valid', 'valid', 'valid@lutece.fr', 0, 'adminadmin', 'fr', 3, 0, 0, NULL, NULL, 0, '1980-01-01 00:00:00');
/*!40000 ALTER TABLE `core_admin_user` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_user_anonymize_field
DROP TABLE IF EXISTS `core_admin_user_anonymize_field`;
CREATE TABLE IF NOT EXISTS `core_admin_user_anonymize_field` (
  `field_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `anonymize` smallint(6) NOT NULL,
  PRIMARY KEY (`field_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_user_anonymize_field: 4 rows
/*!40000 ALTER TABLE `core_admin_user_anonymize_field` DISABLE KEYS */;
INSERT INTO `core_admin_user_anonymize_field` (`field_name`, `anonymize`) VALUES
	('access_code', 1),
	('last_name', 1),
	('first_name', 1),
	('email', 1);
/*!40000 ALTER TABLE `core_admin_user_anonymize_field` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_user_field
DROP TABLE IF EXISTS `core_admin_user_field`;
CREATE TABLE IF NOT EXISTS `core_admin_user_field` (
  `id_user_field` int(11) NOT NULL DEFAULT '0',
  `id_user` int(11) DEFAULT NULL,
  `id_attribute` int(11) DEFAULT NULL,
  `id_field` int(11) DEFAULT NULL,
  `id_file` int(11) DEFAULT NULL,
  `user_field_value` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id_user_field`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_user_field: 0 rows
/*!40000 ALTER TABLE `core_admin_user_field` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_admin_user_field` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_user_preferences
DROP TABLE IF EXISTS `core_admin_user_preferences`;
CREATE TABLE IF NOT EXISTS `core_admin_user_preferences` (
  `id_user` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `pref_key` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `pref_value` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id_user`,`pref_key`),
  KEY `index_admin_user_preferences` (`id_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_user_preferences: 0 rows
/*!40000 ALTER TABLE `core_admin_user_preferences` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_admin_user_preferences` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_workgroup
DROP TABLE IF EXISTS `core_admin_workgroup`;
CREATE TABLE IF NOT EXISTS `core_admin_workgroup` (
  `workgroup_key` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `workgroup_description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`workgroup_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_workgroup: 0 rows
/*!40000 ALTER TABLE `core_admin_workgroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_admin_workgroup` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_admin_workgroup_user
DROP TABLE IF EXISTS `core_admin_workgroup_user`;
CREATE TABLE IF NOT EXISTS `core_admin_workgroup_user` (
  `workgroup_key` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `id_user` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`workgroup_key`,`id_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_admin_workgroup_user: 0 rows
/*!40000 ALTER TABLE `core_admin_workgroup_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_admin_workgroup_user` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_attribute
DROP TABLE IF EXISTS `core_attribute`;
CREATE TABLE IF NOT EXISTS `core_attribute` (
  `id_attribute` int(11) NOT NULL DEFAULT '0',
  `type_class_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` mediumtext COLLATE utf8_unicode_ci,
  `help_message` mediumtext COLLATE utf8_unicode_ci,
  `is_mandatory` smallint(6) DEFAULT '0',
  `is_shown_in_search` smallint(6) DEFAULT '0',
  `is_shown_in_result_list` smallint(6) DEFAULT '0',
  `is_field_in_line` smallint(6) DEFAULT '0',
  `attribute_position` int(11) DEFAULT '0',
  `plugin_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `anonymize` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id_attribute`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_attribute: 0 rows
/*!40000 ALTER TABLE `core_attribute` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_attribute` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_attribute_field
DROP TABLE IF EXISTS `core_attribute_field`;
CREATE TABLE IF NOT EXISTS `core_attribute_field` (
  `id_field` int(11) NOT NULL DEFAULT '0',
  `id_attribute` int(11) DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DEFAULT_value` mediumtext COLLATE utf8_unicode_ci,
  `is_DEFAULT_value` smallint(6) DEFAULT '0',
  `height` int(11) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `max_size_enter` int(11) DEFAULT NULL,
  `is_multiple` smallint(6) DEFAULT '0',
  `field_position` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_field`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_attribute_field: 0 rows
/*!40000 ALTER TABLE `core_attribute_field` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_attribute_field` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_connections_log
DROP TABLE IF EXISTS `core_connections_log`;
CREATE TABLE IF NOT EXISTS `core_connections_log` (
  `access_code` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ip_address` varchar(63) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_login` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `login_status` int(11) DEFAULT NULL,
  KEY `index_connections_log` (`ip_address`,`date_login`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_connections_log: 0 rows
/*!40000 ALTER TABLE `core_connections_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_connections_log` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_dashboard
DROP TABLE IF EXISTS `core_dashboard`;
CREATE TABLE IF NOT EXISTS `core_dashboard` (
  `dashboard_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `dashboard_column` int(11) NOT NULL,
  `dashboard_order` int(11) NOT NULL,
  PRIMARY KEY (`dashboard_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_dashboard: 4 rows
/*!40000 ALTER TABLE `core_dashboard` DISABLE KEYS */;
INSERT INTO `core_dashboard` (`dashboard_name`, `dashboard_column`, `dashboard_order`) VALUES
	('CORE_SYSTEM', 1, 3),
	('CORE_USERS', 1, 1),
	('CORE_USER', 4, 1),
	('CORE_PAGES', 1, 2);
/*!40000 ALTER TABLE `core_dashboard` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_datastore
DROP TABLE IF EXISTS `core_datastore`;
CREATE TABLE IF NOT EXISTS `core_datastore` (
  `entity_key` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `entity_value` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`entity_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_datastore: 63 rows
/*!40000 ALTER TABLE `core_datastore` DISABLE KEYS */;
INSERT INTO `core_datastore` (`entity_key`, `entity_value`) VALUES
	('core.backOffice.defaultEditor', 'tinymce'),
	('core.frontOffice.defaultEditor', 'markitupbbcode'),
	('portal.site.site_property.name', 'LUTECE'),
	('portal.site.site_property.meta.author', '<author>'),
	('portal.site.site_property.meta.copyright', '<copyright>'),
	('portal.site.site_property.meta.description', '<description>'),
	('portal.site.site_property.meta.keywords', '<keywords>'),
	('portal.site.site_property.email', '<webmaster email>'),
	('portal.site.site_property.noreply_email', 'no-reply@mydomain.com'),
	('portal.site.site_property.home_url', 'jsp/site/Portal.jsp'),
	('portal.site.site_property.admin_home_url', 'jsp/admin/AdminMenu.jsp'),
	('gtools.site_property.analytics.code', '<Your Google Analytics Code>'),
	('gtools.site_property.webmaster_tools.code', '<Your Webmaster Tools Code>'),
	('seo.rewrite.config.lastUpdate', 'Dernière mise à jour du fichier de configuration : 3 oct. 2012 23:31:51 Nombre d\'url : 11 Resultat : OK'),
	('seo.config.uptodate', 'false'),
	('seo.generator.option.addPath', 'false'),
	('seo.generator.option.addHtmlSuffix', 'true'),
	('seo.replaceUrl.enabled', 'true'),
	('seo.generator.daemon.enabled', 'true'),
	('seo.canonicalUrls.enabled', 'true'),
	('seo.sitmap.daemon.enabled', 'true'),
	('seo.sitemap.update.log', 'Dernière génération : 4 oct. 2012 00:29:02 Nombre d\'url : 8 Resultat : OK'),
	('core.cache.status.SiteMapService.enabled', '1'),
	('core.cache.status.StaticFilesCachingFilter.enabled', '1'),
	('core.cache.status.MyPortalWidgetService.enabled', '1'),
	('core.cache.status.MailAttachmentCacheService.timeToLiveSeconds', '7200'),
	('core.cache.status.DocumentResourceServletCache.enabled', '1'),
	('core.cache.status.PageCachingFilter.enabled', '0'),
	('core.cache.status.PortletCacheService.enabled', '0'),
	('core.cache.status.MailAttachmentCacheService.diskPersistent', 'true'),
	('core.cache.status.PageCacheService.enabled', '1'),
	('core.cache.status.MailAttachmentCacheService.maxElementsInMemory', '10'),
	('core.cache.status.MailAttachmentCacheService.overflowToDisk', 'true'),
	('core.cache.status.MailAttachmentCacheService.enabled', '1'),
	('core.cache.status.StaticFilesCachingFilter.timeToLiveSeconds', '604800'),
	('core.cache.status.PortalMenuService.enabled', '1'),
	('core.cache.status.MyPortalWidgetContentService.enabled', '1'),
	('core.plugins.status.core_extensions.installed', 'true'),
	('core.plugins.status.lucene.installed', 'true'),
	('core.startup.time', '9 juil. 2013 15:59:08'),
	('core.cache.status.DatastoreCacheService.enabled', '0'),
	('core.plugins.status.childpages.installed', 'true'),
	('core.plugins.status.contact.installed', 'true'),
	('core.plugins.status.contact.pool', 'portal'),
	('core.plugins.status.extend.installed', 'true'),
	('core.plugins.status.extend.pool', 'portal'),
	('core.plugins.status.extend-comment.installed', 'true'),
	('core.plugins.status.extend-comment.pool', 'portal'),
	('core.plugins.status.extend-feedback.installed', 'true'),
	('core.plugins.status.extend-feedback.pool', 'portal'),
	('core.plugins.status.extend-opengraph.installed', 'true'),
	('core.plugins.status.extend-opengraph.pool', 'portal'),
	('core.plugins.status.gtools.installed', 'true'),
	('core.plugins.status.html.installed', 'true'),
	('core.plugins.status.jcaptcha.installed', 'true'),
	('core.plugins.status.searchstats.installed', 'true'),
	('core.plugins.status.searchstats.pool', 'portal'),
	('core.plugins.status.seo.installed', 'true'),
	('core.plugins.status.seo.pool', 'portal'),
	('core.plugins.status.systeminfo.installed', 'true'),
	('core.plugins.status.theme.installed', 'true'),
	('core.plugins.status.theme.pool', 'portal'),
	('core.cache.status.XMLTransformerCacheService(XSLT).enabled', '1');
/*!40000 ALTER TABLE `core_datastore` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_feature_group
DROP TABLE IF EXISTS `core_feature_group`;
CREATE TABLE IF NOT EXISTS `core_feature_group` (
  `id_feature_group` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `feature_group_description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `feature_group_label` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `feature_group_order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_feature_group`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_feature_group: 7 rows
/*!40000 ALTER TABLE `core_feature_group` DISABLE KEYS */;
INSERT INTO `core_feature_group` (`id_feature_group`, `feature_group_description`, `feature_group_label`, `feature_group_order`) VALUES
	('CONTENT', 'portal.features.group.content.description', 'portal.features.group.content.label', 1),
	('APPLICATIONS', 'portal.features.group.applications.description', 'portal.features.group.applications.label', 3),
	('SYSTEM', 'portal.features.group.system.description', 'portal.features.group.system.label', 7),
	('SITE', 'portal.features.group.site.description', 'portal.features.group.site.label', 2),
	('STYLE', 'portal.features.group.charter.description', 'portal.features.group.charter.label', 6),
	('USERS', 'portal.features.group.users.description', 'portal.features.group.users.label', 4),
	('MANAGERS', 'portal.features.group.managers.description', 'portal.features.group.managers.label', 5);
/*!40000 ALTER TABLE `core_feature_group` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_file
DROP TABLE IF EXISTS `core_file`;
CREATE TABLE IF NOT EXISTS `core_file` (
  `id_file` int(11) NOT NULL DEFAULT '0',
  `title` mediumtext COLLATE utf8_unicode_ci,
  `id_physical_file` int(11) DEFAULT NULL,
  `file_size` int(11) DEFAULT NULL,
  `mime_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_file`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_file: 2 rows
/*!40000 ALTER TABLE `core_file` DISABLE KEYS */;
INSERT INTO `core_file` (`id_file`, `title`, `id_physical_file`, `file_size`, `mime_type`) VALUES
	(125, 'export_users_csv.xml', 125, 2523, 'application/xml'),
	(126, 'export_users_xml.xml', 126, 259, 'application/xml');
/*!40000 ALTER TABLE `core_file` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_id_generator
DROP TABLE IF EXISTS `core_id_generator`;
CREATE TABLE IF NOT EXISTS `core_id_generator` (
  `class_name` varchar(250) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `current_value` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`class_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_id_generator: 0 rows
/*!40000 ALTER TABLE `core_id_generator` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_id_generator` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_indexer_action
DROP TABLE IF EXISTS `core_indexer_action`;
CREATE TABLE IF NOT EXISTS `core_indexer_action` (
  `id_action` int(11) NOT NULL DEFAULT '0',
  `id_document` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `id_task` int(11) NOT NULL DEFAULT '0',
  `indexer_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `id_portlet` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_action`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_indexer_action: 0 rows
/*!40000 ALTER TABLE `core_indexer_action` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_indexer_action` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_level_right
DROP TABLE IF EXISTS `core_level_right`;
CREATE TABLE IF NOT EXISTS `core_level_right` (
  `id_level` smallint(6) NOT NULL DEFAULT '0',
  `name` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_level`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_level_right: 4 rows
/*!40000 ALTER TABLE `core_level_right` DISABLE KEYS */;
INSERT INTO `core_level_right` (`id_level`, `name`) VALUES
	(0, 'Niveau 0 - Droits de l\'administrateur technique'),
	(1, 'Niveau 1 - Droits de l\'administrateur fonctionnel'),
	(2, 'Niveau 2 - Droits du webmestre'),
	(3, 'Niveau 3 - Droits de l\'assistant webmestre');
/*!40000 ALTER TABLE `core_level_right` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_mail_item
DROP TABLE IF EXISTS `core_mail_item`;
CREATE TABLE IF NOT EXISTS `core_mail_item` (
  `id_mail_queue` int(11) NOT NULL DEFAULT '0',
  `mail_item` mediumblob,
  PRIMARY KEY (`id_mail_queue`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_mail_item: 0 rows
/*!40000 ALTER TABLE `core_mail_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_mail_item` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_mail_queue
DROP TABLE IF EXISTS `core_mail_queue`;
CREATE TABLE IF NOT EXISTS `core_mail_queue` (
  `id_mail_queue` int(11) NOT NULL DEFAULT '0',
  `is_locked` smallint(6) DEFAULT '0',
  PRIMARY KEY (`id_mail_queue`),
  KEY `is_locked_core_mail_queue` (`is_locked`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_mail_queue: 0 rows
/*!40000 ALTER TABLE `core_mail_queue` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_mail_queue` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_mode
DROP TABLE IF EXISTS `core_mode`;
CREATE TABLE IF NOT EXISTS `core_mode` (
  `id_mode` int(11) NOT NULL DEFAULT '0',
  `description_mode` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `path` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `output_xsl_method` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `output_xsl_version` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `output_xsl_media_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `output_xsl_encoding` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `output_xsl_indent` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `output_xsl_omit_xml_dec` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `output_xsl_standalone` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_mode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_mode: 3 rows
/*!40000 ALTER TABLE `core_mode` DISABLE KEYS */;
INSERT INTO `core_mode` (`id_mode`, `description_mode`, `path`, `output_xsl_method`, `output_xsl_version`, `output_xsl_media_type`, `output_xsl_encoding`, `output_xsl_indent`, `output_xsl_omit_xml_dec`, `output_xsl_standalone`) VALUES
	(0, 'Normal', 'normal/', 'xml', '1.0', 'text/xml', 'UTF-8', 'yes', 'yes', 'yes'),
	(1, 'Administration', 'admin/', 'xml', '1.0', 'text/xml', 'UTF-8', 'yes', 'yes', 'yes'),
	(2, 'Wap', 'wml/', 'xml', '1.0', 'text/xml', 'UTF-8', 'yes', 'yes', 'yes');
/*!40000 ALTER TABLE `core_mode` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_page
DROP TABLE IF EXISTS `core_page`;
CREATE TABLE IF NOT EXISTS `core_page` (
  `id_page` int(11) NOT NULL DEFAULT '0',
  `id_parent` int(11) DEFAULT '0',
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `description` mediumtext COLLATE utf8_unicode_ci,
  `date_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` smallint(6) DEFAULT NULL,
  `page_order` int(11) DEFAULT '0',
  `id_template` int(11) DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `role` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `code_theme` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `node_status` smallint(6) NOT NULL DEFAULT '1',
  `image_content` mediumblob,
  `mime_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT 'NULL',
  `meta_keywords` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `meta_description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id_authorization_node` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_page`),
  KEY `index_page` (`id_template`,`id_parent`),
  KEY `index_childpage` (`id_parent`,`page_order`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_page: 8 rows
/*!40000 ALTER TABLE `core_page` DISABLE KEYS */;
INSERT INTO `core_page` (`id_page`, `id_parent`, `name`, `description`, `date_update`, `status`, `page_order`, `id_template`, `date_creation`, `role`, `code_theme`, `node_status`, `image_content`, `mime_type`, `meta_keywords`, `meta_description`, `id_authorization_node`) VALUES
	(1, 0, 'accueil', 'Page d\'accueil', '2012-10-10 10:20:26', 1, 1, 5, '2003-09-09 02:38:01', 'none', 'default', 0, _binary '', 'application/octet-stream', NULL, NULL, 1),
	(3, 1, 'Documentation', 'Tout ce dont vous avez besoin pour utiliser Lutece', '2006-10-18 11:39:24', 0, 2, 2, '2002-09-09 02:46:46', 'none', 'default', 0, _binary '', 'application/octet-stream', NULL, NULL, 1),
	(6, 3, 'Guide utilisateur', 'Accès au guide utilisateur', '2006-09-19 10:20:13', 0, 1, 1, '2006-02-15 14:39:59', 'none', 'default', 1, NULL, '', NULL, NULL, 1),
	(5, 1, 'L\'outil', 'Description du CMS Lutèce', '2012-10-10 14:03:47', 0, 1, 1, '2006-02-15 14:37:26', 'none', 'default', 1, NULL, '', NULL, NULL, 1),
	(7, 3, 'Guide technique', 'Accès à documentation technique', '2006-09-19 10:19:45', 0, 2, 1, '2006-02-15 14:40:30', 'none', 'default', 1, _binary 0x47494638396130003000C3B700000402047CE2809AEFBFBD3F44424454527CC384C382C2BCC2A4C2A2C2A46C6AE2809E5C5E5C2422243C426CC3A4C3A2C39C746EEFBFBD3FEFBFBD3FE28099EFBFBD3F343234C2B4C2B2C2B4545264C394C392C38C1412145452545C5E7C7C7A7CC3B4C3B2C3ACC2A4C2A2C2B4EFBFBD3FE28099C2AC3432444442542C2A2C7C7AEFBFBD3FE2809EE2809AC2A46466C5927472E2809E4C4E64C2BCC2BAC2BC545274C39CC39AC39C0D0A0A0D0AC384C386C38C747674C3A4C3A6C3ACC592E28099C2A41C1A1C64667CC2ACC2AAC2AC6C6AC5925C5E747476C592C3BCC3BAC3B4C2ACC2AAC2B43C3A444C4A4C545A7C2426347476EFBFBD3F3C3A3C5C5A64C593C5BEC2AC4C4A542C2A347C7EC2A4C592C5BDC2A4444A74C592C5A0C593C2A4C2A2C2AC24222C7472C593C2B4C2B6C384C39CC39AC3945C5A5C5C5EE2809E7C7AC593C2BCC2BAC384C39CC39EC3A40D0A0E14C38CC38EC38CC3ACC3AEC3ACC593C5A1C2A41C1A246C6A6CC2ACC2AAC2BC04060D0AE2809EE280A0C59344424CC384C382C3846C6EE2809E44466CC3A4C3A2C3A46C72EFBFBD3FC593C5A1C59334323CC2B4C2B2C2BC54526CC394C392C39414161C54525C7C7E7CC3B4C3B2C3B4EFBFBD3FE28099C2B43436445C5A74C39CC39EC39CEFBFBD3FE28093C2A46466E2809E6C6EC592646274747AC592C3BCC3BAC3BC3C3A4C5C5AE2809E4C4A5C2C2E34C592C5A0C2AC4C4E74040604E2809EE2809AEFBFBD3F44464454567CC2A4C2A6C2A464666424262444426CEFBFBD3FE28093EFBFBD3F343634C2B4C2B6C2B45C566414161454565464627C7476E2809EC2A4C2A6C2B44C4A6C7472C5925C5A6CC593C5BEC2B4C38CC38EC394C3ACC3AEC3B4C38CC38AC38CC3ACC3AAC3AC6462E2809EEFBFBD3FE28093C2AC4446542C2E2C7C7EEFBFBD3FE2809EE280A0C2A4C2BCC2BEC2BC5456740D0A0E0D0A1C1E1CC2ACC2AEC2ACC2ACC2AEC2B44C4E4C3C3E3CC2A4C2A6C2AC24262C7C7EC593C2BCC2BEC3841C1E24C2ACC2AEC2BCC384C386C384C3A4C3A6C3A4C394C396C394C3B4C3B6C3B4C3BCC3BEC3BC3C3E4C4C4E5CC592C5BDC2AC6C66C592EFBFBD3FE28099C2A46C667C645E747C76C5925C5A7C4C4A74140E14746EE2809E7472EFBFBD3F3C3644C3A4C39EC39C746EC592342E347C7CC3BF00704800C3800015120000000000C382C2A0002AC3AE00E2809A12007C0020000060000015000000000000C3A8780152EFBFBD3F00161200000000C2BE08003EC2B500E2809A4B007C00577D58C3B604EFBFBD3FE282AC00127C00005C74C3B3C380EFBFBD3FC2B212124E00000020C3B7C592603EEFBFBD3F15E2809A12007C006904C2BE5CC3B03E4D4EE2809A65007C730D0A5020C3B0C384644E126F00006300C2B67501C3BF6D00C3BF65007F6E700874C380C3847312125C00004D00C3A86501527300162000006916C2BE6D3F3E61E2809AE2809A677C7C6500C3A87300525C00160000000000000000000100000000000100C2AF000049020047000000C2A0C5BE080001C384001E120001001F00080000C38400001200000021C3B90401000000002C00000000300030000708C3BF0001081C48C2B0C2A0EFBFBD3FC69208132A5CC388C2B0C2A1C383E280A110234AC59348C2B1C2A2C385E2809A58305DC2ACCB86644F070F7D2830685262C2A3C3830606CB86C3B410C2A20454C5A134C2A13AC3B131E284A2C2B063E280A13259EFBFBD3F78320133EFBFBD3FC2A13135681E6CC2B06242C5934F15C2AA7C09C385C2B4C38A2310C592E2809E121C61C2A3C3A80D0A25CB863CC3B54CC3B309E2809EC5BE470DC2A40A6C2368EFBFBD3F20C2A45510310DC2A5C2A4C393531050C2A5525D00C3A906C39623C2A0CB9CC2A6EFBFBD3F2545C393233DE282AC35086DC393E2809A48E284A242C2A0C392C2AEC3BDC2B245C5A01402701DC3A811C2BC71C3841E1A217628C2A9306669C2A834C5BEE2809974C3AA24C3A5C2A91EC389EFBFBD3F2D626AC39141E280A211174A44C3A80525C3A2EFBFBD3F21C392EFBFBD3FC3BEC3AAE284A2C3A4C380C38E460FE280A0C2B728EFBFBD3FC2A9C39405C2A22D49E28099C39C2EC3ADC395EFBFBD3FC2A4490836C3A2486440C38416C2AC55EFBFBD3F54C39902C2A1EFBFBD3F72C388201C38C3BF5031C389C3B7C3851CC2AE0275C3BAC3A409E2809802C3B75BEFBFBD3F2F37C3ADC593C2BCC2A4C38A2DC3AE00C3BA54C385535A05C3B2EFBFBD3FC3A65773E2809CC2A8C2A042741BEFBFBD3F11C38206C5B8C592EFBFBD3F487F4704C388C39C69EFBFBD3FC391C2A1C3827D1B45C391C39A2122C3B8C3A7092CC38A09485FEFBFBD3F1662781102E2809A50E28098E280A61026C592C3A1C38918214E58C5B80A16C2A260121C065071027F555431E280A06DC2B8114823EFBFBD3FE28099C380EFBFBD3F0202C5926021400D0A120D0A31C38401434860C3894C0A0D32C38714101CC2A14015C2B50509C3987334C392C3B115E280A1C3AD55C3A0C3925A68C2AAC2B0500D1D0422E280A602631CC3B1C3896832567809085B74CB9C15227C22C2A2E2809E125F7CE2809857270EC3A4C2A1101F66C39CC3A1032C47C5922102697EEFBFBD3FC3A6C593E280A6EFBFBD3F24EFBFBD3F5F7BC3ADC3B95941C2A0671E5200085E2CC3A44720EFBFBD3FC59261C3AA27C5BDEFBFBD3F48C5BE14E28093C3826242C2A67E06C3BF2A284CE280A1EFBFBD3FC3A1C5931E7FC2B0C3800542C2A3C38C31EFBFBD3F16C2A63646E282AC6EC3A3C3A921C385215B1CC3A1C389C2B27E6EC38629C2AD743CC3A7002517C2B0E28098501B655001022CC3963DC2A209EFBFBD3FEFBFBD3F48C39109C2B0C38CC3B2C3B927C2A779C395C38AE280BA783B68C2A1502406C39C71C692C2A35BC3A476C39A57C3A226C39121C2A6EFBFBD3F3E1B4AC2ADC38E49664A19702C34080F2DC592C3B14921C2A6EFBFBD3FC3A0CB9C1410CB86EFBFBD3F5FC2A64A18C2B2C2A9C2A0C3BF1620C2AD1E64C2B8C2B2C3AB42C2A2C2AC21E280A0080A240157C2B804C2B07A29C2ACC38E7E011309C3914E42E280B01EC5A014C2A111430864E280BA0925E280A17CE280A2E280BA26E280A17CC2A2C2AC09C3A61AC3A26F271AC38BC2AC47013AC380C3A0101C2CE2809E10C3881B3B702BE2809A0863C3B4C2B8C3ACC3965C7BC2A2E2809EC2A7EFBFBD3F4DC2A2C387251CC59202510E2BC388EFBFBD3FCB861526E282ACC3B26756C38BC3B6C3A8C2A3C2A9577F22E2809A1EC3A44946360D0A12E280B0C3BFC3A2C5A0150D0A0421E2809AC2B2E284A2C3BA67C2AAC2A357E280B960C2B714C3A4C3890D0AE280A619E280984CEFBFBD3F431945C3A8C3A00829C5A010C382E280B011241472C3B5C3A16308C3B1C3892749C2AC0D0A45114C58C2B40916C2A2C2B021E280A01F6600E2809809073B64C3AE4416C5A1EFBFBD3FE282ACC3AC160438EFBFBD3FC6920E6D4804070D0AE280981B0447245C60E2809A45061FCB8651E280A01945EFBFBD3F7E01214EC3ACC3804106126DC3924A2213EFBFBD3FEFBFBD3FC380080D0AEFBFBD3FEFBFBD3F040ACB9CE2809EEFBFBD3FC2BC18E2809A3C20C3912234C38CC391CB8627C2A1C3B8C2B8E280A61E57C39421E280A10628E282ACC2BF50EFBFBD3F10C2A1EFBFBD3FC5A0197378EFBFBD3FC39B44EFBFBD3FE2809C507046044978C38424C2AEC3A0E280A63A48200FC3BAC2B3482BC38A30EFBFBD3F4328C3A00D0AC3BE71C38971E282AC44C5A1C387EFBFBD3FC3A629C3A6C2B14817CB8630E280A6315CC3871347EFBFBD3F090424C3B4E2809349E280A267236D480F093EEFBFBD3FC2A7C3A1CB9CEFBFBD3FE280A65EC39103250A64C2A2C5A044E2809A065478EFBFBD3F101FC392C3A2C2A0C3AD24C2A7C692C2A601C393EFBFBD3F4CC2A2C2A04C34C3883D265040216244C5B8C3B1EFBFBD3FC2A8220101003B, 'image/gif', NULL, NULL, 1),
	(10, 1, 'Développeurs', 'Ressources pour les contributeurs/développeurs Lutèce', '2009-05-01 20:25:13', 0, 4, 2, '2006-10-12 11:03:20', 'none', 'default', 1, NULL, NULL, NULL, NULL, 1),
	(11, 5, 'Répondez à notre questionnaire', 'Plugin form', '2009-06-16 08:54:35', 0, 1, 2, '2009-06-16 08:53:39', 'none', 'default', 1, NULL, NULL, NULL, NULL, 1),
	(12, 10, 'Générateur de code', '', '2009-07-13 11:49:14', 0, 1, 1, '2009-07-13 11:49:14', 'none', 'default', 1, NULL, NULL, NULL, NULL, 1);
/*!40000 ALTER TABLE `core_page` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_page_template
DROP TABLE IF EXISTS `core_page_template`;
CREATE TABLE IF NOT EXISTS `core_page_template` (
  `id_template` int(11) NOT NULL DEFAULT '0',
  `description` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `file_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `picture` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_template`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_page_template: 6 rows
/*!40000 ALTER TABLE `core_page_template` DISABLE KEYS */;
INSERT INTO `core_page_template` (`id_template`, `description`, `file_name`, `picture`) VALUES
	(1, 'Une colonne', 'skin/site/page_template1.html', 'page_template1.gif'),
	(2, 'Deux colonnes', 'skin/site/page_template2.html', 'page_template2.gif'),
	(3, 'Trois colonnes', 'skin/site/page_template3.html', 'page_template3.gif'),
	(4, '1 + 2 colonnes', 'skin/site/page_template4.html', 'page_template4.gif'),
	(5, 'Deux colonnes égales', 'skin/site/page_template5.html', 'page_template5.gif'),
	(6, 'Trois colonnes inégales', 'skin/site/page_template6.html', 'page_template6.gif');
/*!40000 ALTER TABLE `core_page_template` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_physical_file
DROP TABLE IF EXISTS `core_physical_file`;
CREATE TABLE IF NOT EXISTS `core_physical_file` (
  `id_physical_file` int(11) NOT NULL DEFAULT '0',
  `file_value` mediumblob,
  PRIMARY KEY (`id_physical_file`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_physical_file: 2 rows
/*!40000 ALTER TABLE `core_physical_file` DISABLE KEYS */;
INSERT INTO `core_physical_file` (`id_physical_file`, `file_value`) VALUES
	(125, _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A093C78736C3A6F7574707574206D6574686F643D2274657874222F3E0D0A090D0A093C78736C3A74656D706C617465206D617463683D227573657273223E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D227573657222202F3E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D2275736572223E0D0A09093C78736C3A746578743E223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226163636573735F636F646522202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226C6173745F6E616D6522202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D2266697273745F6E616D6522202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D22656D61696C22202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D2273746174757322202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226C6F63616C6522202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226C6576656C22202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226D7573745F6368616E67655F70617373776F726422202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226163636573736962696C6974795F6D6F646522202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D2270617373776F72645F6D61785F76616C69645F6461746522202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226163636F756E745F6D61785F76616C69645F6461746522202F3E0D0A09093C78736C3A746578743E223B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D22646174655F6C6173745F6C6F67696E22202F3E0D0A09093C78736C3A746578743E223C2F78736C3A746578743E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22726F6C657322202F3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D2272696768747322202F3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22776F726B67726F75707322202F3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226174747269627574657322202F3E0D0A09093C78736C3A746578743E262331303B3C2F78736C3A746578743E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D22726F6C6573223E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22726F6C6522202F3E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D22726F6C65223E0D0A09093C78736C3A746578743E3B22726F6C653A3C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D2263757272656E74282922202F3E0D0A09093C78736C3A746578743E223C2F78736C3A746578743E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D22726967687473223E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22726967687422202F3E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D227269676874223E0D0A09093C78736C3A746578743E3B2272696768743A3C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D2263757272656E74282922202F3E0D0A09093C78736C3A746578743E223C2F78736C3A746578743E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D22776F726B67726F757073223E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22776F726B67726F757022202F3E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D22776F726B67726F7570223E0D0A09093C78736C3A746578743E3B22776F726B67726F75703A3C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D2263757272656E74282922202F3E0D0A09093C78736C3A746578743E223C2F78736C3A746578743E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D2261747472696275746573223E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D2261747472696275746522202F3E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A093C78736C3A74656D706C617465206D617463683D22617474726962757465223E0D0A09093C78736C3A746578743E3B223C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226174747269627574652D696422202F3E0D0A09093C78736C3A746578743E3A3C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226174747269627574652D6669656C642D696422202F3E0D0A09093C78736C3A746578743E3A3C2F78736C3A746578743E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226174747269627574652D76616C756522202F3E0D0A09093C78736C3A746578743E223C2F78736C3A746578743E0D0A093C2F78736C3A74656D706C6174653E0D0A090D0A3C2F78736C3A7374796C6573686565743E),
	(126, _binary 0x3C3F786D6C2076657273696F6E3D22312E3022203F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A093C78736C3A74656D706C617465206D617463683D222F207C20402A207C206E6F64652829223E0D0A09093C78736C3A636F70793E0D0A0909093C78736C3A6170706C792D74656D706C617465732073656C6563743D22402A207C206E6F6465282922202F3E0D0A09093C2F78736C3A636F70793E0D0A093C2F78736C3A74656D706C6174653E0D0A3C2F78736C3A7374796C6573686565743E);
/*!40000 ALTER TABLE `core_physical_file` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_portal_component
DROP TABLE IF EXISTS `core_portal_component`;
CREATE TABLE IF NOT EXISTS `core_portal_component` (
  `id_portal_component` int(11) NOT NULL DEFAULT '0',
  `name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_portal_component`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_portal_component: 9 rows
/*!40000 ALTER TABLE `core_portal_component` DISABLE KEYS */;
INSERT INTO `core_portal_component` (`id_portal_component`, `name`) VALUES
	(0, 'Rubrique'),
	(1, 'Article'),
	(2, 'Rubrique Liste Article'),
	(3, 'Menu Init'),
	(4, 'Menu Principal'),
	(5, 'Chemin Page'),
	(6, 'Plan du site'),
	(7, 'Arborescence'),
	(8, 'Plan du site admin');
/*!40000 ALTER TABLE `core_portal_component` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_portlet
DROP TABLE IF EXISTS `core_portlet`;
CREATE TABLE IF NOT EXISTS `core_portlet` (
  `id_portlet` int(11) NOT NULL DEFAULT '0',
  `id_portlet_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id_page` int(11) DEFAULT NULL,
  `name` varchar(70) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` smallint(6) NOT NULL DEFAULT '0',
  `portlet_order` int(11) DEFAULT NULL,
  `column_no` int(11) DEFAULT NULL,
  `id_style` int(11) DEFAULT NULL,
  `accept_alias` smallint(6) DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `display_portlet_title` int(11) NOT NULL DEFAULT '0',
  `role` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `device_display_flags` int(11) NOT NULL DEFAULT '15',
  PRIMARY KEY (`id_portlet`),
  KEY `index_portlet` (`id_page`,`id_portlet_type`,`id_style`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_portlet: 18 rows
/*!40000 ALTER TABLE `core_portlet` DISABLE KEYS */;
INSERT INTO `core_portlet` (`id_portlet`, `id_portlet_type`, `id_page`, `name`, `date_update`, `status`, `portlet_order`, `column_no`, `id_style`, `accept_alias`, `date_creation`, `display_portlet_title`, `role`, `device_display_flags`) VALUES
	(85, 'CHILDPAGES_PORTLET', 5, 'Pages filles', '2007-11-24 17:15:10', 0, 1, 5, 300, 0, '2007-11-24 17:14:58', 1, NULL, 15),
	(87, 'CHILDPAGES_PORTLET', 3, 'Pages filles', '2007-11-24 17:21:01', 0, 1, 5, 300, 0, '2007-11-24 17:19:50', 1, NULL, 15),
	(88, 'CHILDPAGES_PORTLET', 10, 'Pages filles', '2007-11-24 17:20:37', 0, 1, 5, 301, 0, '2007-11-24 17:20:37', 1, NULL, 15),
	(89, 'CHILDPAGES_PORTLET', 9, 'Pages filles', '2007-11-24 17:23:06', 0, 1, 5, 301, 0, '2007-11-24 17:21:47', 1, NULL, 15),
	(83, 'CHILDPAGES_PORTLET', 1, 'Pages filles', '2007-11-24 16:11:33', 0, 1, 5, 300, 0, '2007-11-24 16:11:33', 1, NULL, 15),
	(57, 'HTML_PORTLET', 5, 'Le projet', '2012-10-10 12:40:51', 0, 2, 1, 101, 0, '2011-03-14 14:17:30', 1, 'none', 4369),
	(55, 'HTML_PORTLET', 1, 'Qu\'est-ce que Lutece ?', '2012-09-18 11:10:23', 0, 1, 1, 101, 0, '2011-03-14 14:13:39', 0, 'none', 4369),
	(61, 'HTML_PORTLET', 9, 'Publication d\'agendas', '2011-11-24 15:24:11', 0, 1, 1, 101, 0, '2011-03-14 14:35:35', 0, NULL, 4369),
	(64, 'HTML_PORTLET', 10, 'Infos développeurs', '2011-11-24 15:26:41', 0, 1, 1, 101, 0, '2011-03-14 14:45:14', 0, NULL, 4369),
	(58, 'HTML_PORTLET', 3, 'Accès à la documentation technique', '2012-10-10 14:26:43', 0, 2, 1, 101, 0, '2011-03-14 14:20:08', 1, 'none', 4369),
	(66, 'HTML_PORTLET', 10, 'Tests unitaires', '2011-11-24 15:26:24', 0, 2, 3, 101, 0, '2011-03-14 15:10:26', 0, NULL, 4369),
	(99, 'HTML_PORTLET', 3, 'Illustration', '2012-10-10 14:34:10', 0, 1, 2, 100, 0, '2012-10-10 14:34:10', 1, 'none', 4369),
	(91, 'HTML_PORTLET', 1, 'Bienvenue sur la démo', '2012-09-18 11:18:36', 0, 1, 2, 100, 0, '2009-05-15 06:38:08', 0, 'none', 4369),
	(92, 'HTML_PORTLET', 1, 'Qui utilise Lutèce ?', '2012-09-18 10:34:28', 0, 2, 1, 100, 0, '2009-05-19 10:21:02', 0, 'none', 4369),
	(95, 'HTML_PORTLET', 6, 'Ajouter du contenu dans Lutece', '2009-06-17 05:06:58', 0, 1, 1, 100, 0, '2009-06-17 05:06:58', 1, NULL, 4369),
	(96, 'HTML_PORTLET', 11, 'Info', '2009-06-24 06:47:26', 0, 1, 2, 100, 0, '2009-06-24 06:42:42', 1, NULL, 4369),
	(97, 'HTML_PORTLET', 12, 'Générateur de code', '2009-07-13 09:50:26', 0, 1, 1, 100, 0, '2009-07-13 09:50:26', 0, NULL, 4369),
	(98, 'HTML_PORTLET', 1, 'Nouveautés de la version 4.0', '2012-10-10 14:00:44', 0, 1, 2, 100, 0, '2012-09-18 10:35:45', 0, 'none', 4369);
/*!40000 ALTER TABLE `core_portlet` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_portlet_alias
DROP TABLE IF EXISTS `core_portlet_alias`;
CREATE TABLE IF NOT EXISTS `core_portlet_alias` (
  `id_portlet` int(11) NOT NULL DEFAULT '0',
  `id_alias` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_portlet`,`id_alias`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_portlet_alias: 0 rows
/*!40000 ALTER TABLE `core_portlet_alias` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_portlet_alias` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_portlet_type
DROP TABLE IF EXISTS `core_portlet_type`;
CREATE TABLE IF NOT EXISTS `core_portlet_type` (
  `id_portlet_type` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0',
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url_creation` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url_update` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `home_class` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `plugin_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url_docreate` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `create_script` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `create_specific` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `create_specific_form` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url_domodify` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `modify_script` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `modify_specific` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `modify_specific_form` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_portlet_type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_portlet_type: 3 rows
/*!40000 ALTER TABLE `core_portlet_type` DISABLE KEYS */;
INSERT INTO `core_portlet_type` (`id_portlet_type`, `name`, `url_creation`, `url_update`, `home_class`, `plugin_name`, `url_docreate`, `create_script`, `create_specific`, `create_specific_form`, `url_domodify`, `modify_script`, `modify_specific`, `modify_specific_form`) VALUES
	('ALIAS_PORTLET', 'portal.site.portletAlias.name', 'plugins/alias/CreatePortletAlias.jsp', 'plugins/alias/ModifyPortletAlias.jsp', 'fr.paris.lutece.portal.business.portlet.AliasPortletHome', 'alias', 'plugins/alias/DoCreatePortletAlias.jsp', '/admin/portlet/script_create_portlet.html', '/admin/portlet/alias/create_portlet_alias.html', '', 'plugins/alias/DoModifyPortletAlias.jsp', '/admin/portlet/script_modify_portlet.html', '/admin/portlet/alias/modify_portlet_alias.html', ''),
	('CHILDPAGES_PORTLET', 'childpages.portlet.name', 'plugins/childpages/CreatePortletChildPages.jsp', 'plugins/childpages/ModifyPortletChildPages.jsp', 'fr.paris.lutece.plugins.childpages.business.portlet.ChildPagesPortletHome', 'childpages', 'plugins/childpages/DoCreatePortletChildPages.jsp', '/admin/portlet/script_create_portlet.html', '/admin/plugins/childpages/value_id_parent.html', '', 'plugins/childpages/DoModifyPortletChildPages.jsp', '/admin/portlet/script_modify_portlet.html', '/admin/plugins/childpages/value_id_parent.html', ''),
	('HTML_PORTLET', 'html.portlet.name', 'plugins/html/CreatePortletHtml.jsp', 'plugins/html/ModifyPortletHtml.jsp', 'fr.paris.lutece.plugins.html.business.portlet.HtmlPortletHome', 'html', 'plugins/html/DoCreatePortletHtml.jsp', '/admin/portlet/script_create_portlet.html', '/admin/plugins/html/portlet_html.html', '', 'plugins/html/DoModifyPortletHtml.jsp', '/admin/portlet/script_modify_portlet.html', '/admin/plugins/html/portlet_html.html', '');
/*!40000 ALTER TABLE `core_portlet_type` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_role
DROP TABLE IF EXISTS `core_role`;
CREATE TABLE IF NOT EXISTS `core_role` (
  `role` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `role_description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `workgroup_key` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`role`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_role: 0 rows
/*!40000 ALTER TABLE `core_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_role` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_search_parameter
DROP TABLE IF EXISTS `core_search_parameter`;
CREATE TABLE IF NOT EXISTS `core_search_parameter` (
  `parameter_key` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `parameter_value` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`parameter_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_search_parameter: 6 rows
/*!40000 ALTER TABLE `core_search_parameter` DISABLE KEYS */;
INSERT INTO `core_search_parameter` (`parameter_key`, `parameter_value`) VALUES
	('type_filter', 'none'),
	('default_operator', 'OR'),
	('help_message', 'Message d aide pour la recherche'),
	('date_filter', '0'),
	('tag_filter', '0'),
	('taglist', NULL);
/*!40000 ALTER TABLE `core_search_parameter` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_style
DROP TABLE IF EXISTS `core_style`;
CREATE TABLE IF NOT EXISTS `core_style` (
  `id_style` int(11) NOT NULL DEFAULT '0',
  `description_style` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `id_portlet_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id_portal_component` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_style`),
  KEY `index_style` (`id_portlet_type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_style: 10 rows
/*!40000 ALTER TABLE `core_style` DISABLE KEYS */;
INSERT INTO `core_style` (`id_style`, `description_style`, `id_portlet_type`, `id_portal_component`) VALUES
	(3, 'Menu Init', '', 3),
	(4, 'Main Menu', '', 4),
	(5, 'Chemin Page', '', 5),
	(6, 'Plan du site', '', 6),
	(7, 'Arborescence', '', 7),
	(8, 'Plan du Site Admin', NULL, 8),
	(300, 'Défaut', 'CHILDPAGES_PORTLET', 0),
	(301, 'Image + lien', 'CHILDPAGES_PORTLET', 0),
	(100, 'Défaut', 'HTML_PORTLET', 0),
	(101, 'Fond coloré', 'HTML_PORTLET', 0);
/*!40000 ALTER TABLE `core_style` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_stylesheet
DROP TABLE IF EXISTS `core_stylesheet`;
CREATE TABLE IF NOT EXISTS `core_stylesheet` (
  `id_stylesheet` int(11) NOT NULL DEFAULT '0',
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `file_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source` mediumblob,
  PRIMARY KEY (`id_stylesheet`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_stylesheet: 10 rows
/*!40000 ALTER TABLE `core_stylesheet` DISABLE KEYS */;
INSERT INTO `core_stylesheet` (`id_stylesheet`, `description`, `file_name`, `source`) VALUES
	(253, 'Pages filles - Arborescence', 'menu_tree.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A0D0A3C78736C3A706172616D206E616D653D22736974652D70617468222073656C6563743D22736974652D7061746822202F3E0D0A0D0A3C78736C3A74656D706C617465206D617463683D226D656E752D6C697374223E0D0A093C78736C3A7661726961626C65206E616D653D226D656E752D6C697374222073656C6563743D226D656E7522202F3E0D0A0D0A093C73637269707420747970653D22746578742F6A617661736372697074223E0D0A09092428646F63756D656E74292E72656164792866756E6374696F6E28297B0D0A090909242822237472656522292E7472656576696577287B0D0A09090909616E696D617465643A202266617374222C0D0A09090909636F6C6C61707365643A2066616C73652C0D0A09090909756E697175653A20747275652C0D0A09090909706572736973743A2022636F6F6B6965220D0A0909097D293B0D0A09090D0A09097D293B0D0A093C2F7363726970743E202020200D0A090D0A093C212D2D204D656E752054726565202D2D3E2020202020200D0A093C78736C3A696620746573743D226E6F7428737472696E67286D656E75293D272729223E0D0A09202020203C78736C3A746578742064697361626C652D6F75747075742D6573636170696E673D22796573223E0909202020200D0A2020202020202020202020203C64697620636C6173733D227472656534223E09090D0A0909093C68323E26233136303B3C2F68323E0D0A0909093C756C2069643D22747265652220636C6173733D227472656534223E0D0A202020202020202020202020202020203C78736C3A6170706C792D74656D706C617465732073656C6563743D226D656E7522202F3E20202020202020200D0A0909093C2F756C3E090D0A0909093C2F6469763E0D0A09092009203C6272202F3E0D0A09093C2F78736C3A746578743E200D0A093C2F78736C3A69663E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D226D656E75223E0D0A202020203C78736C3A7661726961626C65206E616D653D22696E646578223E0D0A20202020093C78736C3A6E756D626572206C6576656C3D2273696E676C65222076616C75653D22706F736974696F6E282922202F3E0D0A202020203C2F78736C3A7661726961626C653E0D0A09093C6C693E0D0A202020203C212D2D3C78736C3A696620746573743D2224696E64657820266C743B2037223E2D2D3E20202020202020200D0A202020202020202020203C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207461726765743D225F746F7022203E0D0A2020202020202020202020202020203C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A20202020202020202020203C2F613E092020200D0A09092020203C6272202F3E0D0A09092020203C78736C3A76616C75652D6F662073656C6563743D22706167652D6465736372697074696F6E22202F3E0D0A09092020203C212D2D3C78736C3A76616C75652D6F662073656C6563743D22706167652D6465736372697074696F6E22202F3E3C6272202F3E2D2D3E09092020200909090D0A0909093C78736C3A6170706C792D74656D706C617465732073656C6563743D227375626C6576656C2D6D656E752D6C69737422202F3E200D0A0909090D0A09093C2F6C693E20090D0A202020203C212D2D3C2F78736C3A69663E2D2D3E0D0A09090D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C78736C3A74656D706C617465206D617463683D227375626C6576656C2D6D656E752D6C69737422203E200D0A090D0A093C78736C3A6170706C792D74656D706C617465732073656C6563743D227375626C6576656C2D6D656E7522202F3E200920202020090D0A0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D227375626C6576656C2D6D656E75223E0D0A2020203C78736C3A7661726961626C65206E616D653D22696E6465785F736F75735F6D656E75223E0D0A2020202020202020203C78736C3A6E756D626572206C6576656C3D2273696E676C65222076616C75653D22706F736974696F6E282922202F3E0D0A2020203C2F78736C3A7661726961626C653E0D0A0909203C756C203E0D0A0909093C6C693E0D0A3C212D2D093C7370616E3E202D2D3E0D0A090909093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207461726765743D225F746F70223E0D0A09090909093C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A090909093C2F613E0D0A0909093C2F6C693E0909090D0A09093C2F756C3E0D0A093C212D2D3C2F7370616E3E092D2D3E0D0A09090D0A2020200D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C2F78736C3A7374796C6573686565743E0D0A),
	(215, 'Chemin page', 'page_path.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A0D0A3C78736C3A706172616D206E616D653D22736974652D70617468222073656C6563743D22736974652D7061746822202F3E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D2270616765223E0D0A09093C78736C3A696620746573743D22706F736974696F6E2829213D6C61737428292D31223E0D0A0909093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207461726765743D225F746F70223E3C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E3C2F613E203E0D0A09093C2F78736C3A69663E0D0A09093C78736C3A696620746573743D22706F736974696F6E28293D6C61737428292D31223E0D0A0909093C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A09093C2F78736C3A69663E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706167655F6C696E6B223E0D0A09093C78736C3A696620746573743D22706F736974696F6E2829213D6C61737428292D31223E0D0A0909093C6120687265663D227B24736974652D706174687D3F7B706167652D75726C7D22207461726765743D225F746F70223E3C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E3C2F613E203E0D0A09093C2F78736C3A69663E0D0A09093C78736C3A696620746573743D22706F736974696F6E28293D6C61737428292D31223E0D0A0909093C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A09093C2F78736C3A69663E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C2F78736C3A7374796C6573686565743E),
	(213, 'Menu principal', 'menu_main.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E30220D0A09786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A0D0A093C78736C3A706172616D206E616D653D22736974652D70617468222073656C6563743D22736974652D7061746822202F3E0D0A0D0A093C78736C3A74656D706C617465206D617463683D226D656E752D6C697374223E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226D656E7522202F3E0D0A093C2F78736C3A74656D706C6174653E0D0A0D0A093C78736C3A74656D706C617465206D617463683D226D656E75223E0D0A09093C6C693E0D0A0909093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D2220636C6173733D2266697273742D6C6576656C22207461726765743D225F746F70223E0D0A09090909093C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A0909093C2F613E0D0A09093C2F6C693E0D0A093C2F78736C3A74656D706C6174653E0D0A0D0A3C2F78736C3A7374796C6573686565743E0D0A0D0A),
	(211, 'Menu Init', 'menu_init.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A0D0A3C78736C3A706172616D206E616D653D22736974652D70617468222073656C6563743D22736974652D7061746822202F3E0D0A0D0A3C78736C3A74656D706C617465206D617463683D226D656E752D6C697374223E0D0A3C6272202F3E3C6272202F3E0D0A093C6469762069643D226D656E752D696E6974223E0D0A09093C6469762069643D226D656E752D696E69742D636F6E74656E74223E0D0A2020202020202020202020203C756C2069643D226D656E752D7665727469223E0D0A202020202020202020202020202020203C78736C3A6170706C792D74656D706C617465732073656C6563743D226D656E7522202F3E0D0A2020202020202020202020203C2F756C3E0D0A20202020202020203C2F6469763E0D0A20202020203C2F6469763E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D226D656E75223E0D0A202020203C78736C3A7661726961626C65206E616D653D22696E646578223E0D0A20202020093C78736C3A6E756D626572206C6576656C3D2273696E676C65222076616C75653D22706F736974696F6E282922202F3E0D0A202020203C2F78736C3A7661726961626C653E0D0A0D0A202020203C78736C3A696620746573743D2224696E646578202667743B2037223E0D0A20202020202020203C6C6920636C6173733D2266697273742D7665727469223E0D0A2020202020202020093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207461726765743D225F746F70223E0D0A2020202020202020202009093C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A0920202020202020203C2F613E0D0A2020202009202020203C78736C3A6170706C792D74656D706C617465732073656C6563743D227375626C6576656C2D6D656E752D6C69737422202F3E0D0A20202020202020203C2F6C693E0D0A2020203C2F78736C3A69663E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C78736C3A74656D706C617465206D617463683D227375626C6576656C2D6D656E752D6C69737422203E0D0A093C756C3E0D0A20202020093C6C6920636C6173733D226C6173742D7665727469223E0D0A090920093C78736C3A6170706C792D74656D706C617465732073656C6563743D227375626C6576656C2D6D656E7522202F3E0D0A2009202020203C2F6C693E0D0A202020203C2F756C3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C78736C3A74656D706C617465206D617463683D227375626C6576656C2D6D656E75223E0D0A2020203C78736C3A7661726961626C65206E616D653D22696E6465785F736F75735F6D656E75223E0D0A2020202020202020203C78736C3A6E756D626572206C6576656C3D2273696E676C65222076616C75653D22706F736974696F6E282922202F3E0D0A2020203C2F78736C3A7661726961626C653E0D0A0D0A2020203C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207461726765743D225F746F70223E0D0A09093C7370616E3E3C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E3C2F7370616E3E0D0A2020203C2F613E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C2F78736C3A7374796C6573686565743E0D0A),
	(217, 'Plan du site', 'site_map.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E302220656E636F64696E673D2249534F2D383835392D31223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A0D0A3C78736C3A706172616D206E616D653D22736974652D70617468222073656C6563743D22736974652D7061746822202F3E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706167655B706167652D6C6576656C3D305D223E0D0A093C64697620636C6173733D227370616E2D31352070726570656E642D3120617070656E642D3120617070656E642D626F74746F6D223E0D0A09093C64697620636C6173733D22706F72746C6574202D6C75746563652D626F726465722D726164697573223E0D0A0909093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D6C69737422202F3E0D0A09093C2F6469763E0D0A093C2F6469763E0D0A093C6469762069643D22736964656261722220636C6173733D227370616E2D3620617070656E642D3120617070656E642D626F74746F6D206C617374223E0D0A09093C64697620636C6173733D22706F72746C6574202D6C75746563652D626F726465722D726164697573223E0D0A0909093C696D67207372633D22646F63756D656E743F69643D3726616D703B69645F6174747269627574653D35322220616C743D2262616E6E657222207469746C653D2262616E6E6572222F3E0D0A09090926233136303B0D0A09093C2F6469763E0D0A093C2F6469763E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706167655B706167652D6C6576656C3D315D22203E0D0A3C756C20636C6173733D22736974652D6D61702D6C6576656C2D6F6E65223E0D0A093C6C693E0D0A09093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207461726765743D225F746F70223E0D0A0909093C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A09093C2F613E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22706167652D6465736372697074696F6E22202F3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22706167652D696D61676522202F3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D6C69737422202F3E0D0A09202020203C78736C3A746578742064697361626C652D6F75747075742D6573636170696E673D22796573223E0D0A0909202020203C215B43444154415B3C64697620636C6173733D22636C656172223E26233136303B3C2F6469763E5D5D3E0D0A09202020203C2F78736C3A746578743E0D0A093C2F6C693E0D0A3C2F756C3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706167655B706167652D6C6576656C3D325D22203E0D0A3C756C20636C6173733D22736974652D6D61702D6C6576656C2D74776F223E0D0A093C6C693E0D0A09093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207461726765743D225F746F70223E0D0A0909093C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A09093C2F613E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22706167652D6465736372697074696F6E22202F3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D6C69737422202F3E0D0A093C2F6C693E0D0A3C2F756C3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706167655B706167652D6C6576656C3E325D22203E0D0A3C756C20636C6173733D22736974652D6D61702D6C6576656C2D68696768657374223E0D0A093C6C693E0D0A09093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207461726765743D225F746F70223E0D0A0909093C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A09093C2F613E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D22706167652D6465736372697074696F6E22202F3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D6C69737422202F3E0D0A093C2F6C693E0D0A3C2F756C3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706167652D6465736372697074696F6E223E0D0A093C6272202F3E3C78736C3A76616C75652D6F662073656C6563743D222E22202F3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765732D6C6973745B706167652D6C6576656C3D305D223E0D0A093C78736C3A696620746573743D22636F756E742870616765293E3022203E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D227061676522202F3E0D0A202020203C2F78736C3A69663E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765732D6C6973745B706167652D6C6576656C3D315D223E0D0A093C78736C3A696620746573743D22636F756E742870616765293E3022203E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D227061676522202F3E0D0A202020203C2F78736C3A69663E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765732D6C6973745B706167652D6C6576656C3D325D223E0D0A093C78736C3A696620746573743D22636F756E742870616765293E3022203E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D227061676522202F3E0D0A202020203C2F78736C3A69663E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765732D6C6973745B706167652D6C6576656C3E325D223E0D0A093C78736C3A696620746573743D22636F756E742870616765293E3022203E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D227061676522202F3E0D0A202020203C2F78736C3A69663E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706167652D696D616765223E0D0A093C64697620636C6173733D226C6576656C2D6F6E652D696D616765223E0D0A20202020093C64697620636C6173733D22706F6C61726F6964223E0D0A09093C696D672020626F726465723D2230222077696474683D22383022206865696768743D22383022207372633D22696D616765732F6C6F63616C2F646174612F70616765732F7B2E7D2220616C743D2222202F3E0D0A2020202020202020203C2F6469763E0D0A093C2F646976203E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C2F78736C3A7374796C6573686565743E0D0A),
	(279, 'Plan du Site module d\'Administration', 'admin_site_map_admin.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A202020200D0A3C78736C3A706172616D206E616D653D22736974652D70617468222073656C6563743D22736974652D7061746822202F3E0D0A3C78736C3A7661726961626C65206E616D653D2263757272656E742D706167652D6964223E0D0A093C78736C3A76616C75652D6F662073656C6563743D2263757272656E742D706167652D696422202F3E0D0A3C2F78736C3A7661726961626C653E0D0A202020200D0A3C78736C3A74656D706C617465206D617463683D22706167655B706167652D6C6576656C3D305D223E200D0A3C6469762069643D22747265652220636C6173733D226A73747265652D64656661756C74223E0D0A093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207469746C653D227B706167652D6465736372697074696F6E7D22203E0D0A202020203C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A09093C78736C3A696620746573743D226E6F7428737472696E6728706167652D726F6C65293D276E6F6E652729223E200D0A20202020202020203C7374726F6E673E0D0A0909093C78736C3A746578742064697361626C652D6F75747075742D6573636170696E673D22796573223E2D20236931386E7B706F7274616C2E736974652E61646D696E5F706167652E74616241646D696E4D6170526F6C6552657365727665647D3C2F78736C3A746578743E0D0A2020202020202020202020203C78736C3A76616C75652D6F662073656C6563743D22706167652D726F6C6522202F3E0D0A20202020202020203C2F7374726F6E673E0D0A20202020202020203C2F78736C3A69663E2020202020202020202020200D0A202020203C2F613E0D0A202020203C756C3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D6C69737422202F3E0D0A202020203C2F756C3E0D0A3C2F6469763E0D0A3C2F78736C3A74656D706C6174653E0D0A202020200D0A3C78736C3A74656D706C617465206D617463683D22706167655B706167652D6C6576656C3E305D22203E0D0A3C78736C3A7661726961626C65206E616D653D22696E646578223E0D0A093C78736C3A76616C75652D6F662073656C6563743D22706167652D696422202F3E0D0A3C2F78736C3A7661726961626C653E0D0A3C78736C3A7661726961626C65206E616D653D226465736372697074696F6E223E0D0A093C78736C3A76616C75652D6F662073656C6563743D22706167652D6465736372697074696F6E22202F3E0D0A3C2F78736C3A7661726961626C653E0D0A3C6C692069643D226E6F64652D7B24696E6465787D223E0D0A093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B706167652D69647D22207469746C653D227B246465736372697074696F6E7D223E0D0A09093C7374726F6E673E3C78736C3A76616C75652D6F662073656C6563743D22706167652D696422202F3E3C2F7374726F6E673E26233136303B3C78736C3A76616C75652D6F662073656C6563743D22706167652D6E616D6522202F3E0D0A09093C78736C3A696620746573743D226E6F7428737472696E6728706167652D6465736372697074696F6E293D272729223E202D203C78736C3A76616C75652D6F662073656C6563743D22706167652D6465736372697074696F6E22202F3E3C2F78736C3A69663E0D0A09093C78736C3A696620746573743D226E6F7428737472696E6728706167652D726F6C65293D276E6F6E652729223E0D0A0909093C656D3E0D0A090909093C78736C3A746578742064697361626C652D6F75747075742D6573636170696E673D22796573223E236931386E7B706F7274616C2E736974652E61646D696E5F706167652E74616241646D696E4D6170526F6C6552657365727665647D3C2F78736C3A746578743E0D0A202020202020202020202020202020203C78736C3A76616C75652D6F662073656C6563743D22706167652D726F6C6522202F3E0D0A0909093C2F656D3E0D0A20202020202020203C2F78736C3A69663E0D0A202020203C2F613E0D0A093C78736C3A63686F6F73653E0D0A093C78736C3A7768656E20746573743D22636F756E74286368696C642D70616765732D6C6973742F2A293E30223E0D0A202020203C756C3E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D6C69737422202F3E0D0A202020203C2F756C3E0D0A202020203C2F78736C3A7768656E3E0D0A202020203C78736C3A6F74686572776973653E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D6C69737422202F3E0D0A093C2F78736C3A6F74686572776973653E0D0A202020203C2F78736C3A63686F6F73653E0D0A3C2F6C693E0D0A3C2F78736C3A74656D706C6174653E0D0A202020200D0A3C78736C3A74656D706C617465206D617463683D22706167652D6465736372697074696F6E223E0D0A093C78736C3A76616C75652D6F662073656C6563743D222E22202F3E0D0A3C2F78736C3A74656D706C6174653E0D0A202020200D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765732D6C697374223E0D0A093C78736C3A6170706C792D74656D706C617465732073656C6563743D227061676522202F3E0D0A3C2F78736C3A74656D706C6174653E0D0A202020200D0A3C2F78736C3A7374796C6573686565743E),
	(30, 'Rubrique Pages filles - Défaut', 'portlet_childpages_simple.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A0D0A3C78736C3A706172616D206E616D653D22736974652D70617468222073656C6563743D22736974652D7061746822202F3E0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706F72746C6574223E0D0A0D0A093C78736C3A7661726961626C65206E616D653D226465766963655F636C617373223E0D0A093C78736C3A63686F6F73653E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D736D616C6C2D646576696365293D273027223E68696464656E2D70686F6E653C2F78736C3A7768656E3E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D6E6F726D616C2D646576696365293D273027223E68696464656E2D7461626C65743C2F78736C3A7768656E3E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D6C617267652D646576696365293D273027223E68696464656E2D6465736B746F703C2F78736C3A7768656E3E0D0A09093C78736C3A6F74686572776973653E3C2F78736C3A6F74686572776973653E0D0A093C2F78736C3A63686F6F73653E0D0A093C2F78736C3A7661726961626C653E0D0A090D0A093C64697620636C6173733D22706F72746C6574207B246465766963655F636C6173737D223E0D0A20202020202020203C78736C3A696620746573743D226E6F7428737472696E6728646973706C61792D706F72746C65742D7469746C65293D27312729223E0D0A0909093C64697620636C6173733D22706F72746C65742D686561646572202D746F70223E0D0A090909093C78736C3A76616C75652D6F662064697361626C652D6F75747075742D6573636170696E673D22796573222073656C6563743D22706F72746C65742D6E616D6522202F3E0D0A0909093C2F6469763E0D0A20202020202020203C2F78736C3A69663E0D0A09093C78736C3A696620746573743D226E6F7428737472696E6728646973706C61792D706F72746C65742D7469746C65293D27312729223E0D0A0909093C6469763E0D0A090909093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D706F72746C657422202F3E0D0A0909093C2F6469763E0D0A20202020202020203C2F78736C3A69663E0D0A09093C78736C3A696620746573743D22737472696E6728646973706C61792D706F72746C65742D7469746C65293D273127223E0D0A0909093C64697620636C6173733D22706F72746C65742D636F6E74656E74223E0D0A090909093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D706F72746C657422202F3E0D0A0909093C2F6469763E0D0A20202020202020203C2F78736C3A69663E0D0A093C2F6469763E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765732D706F72746C6574223E0D0A093C756C3E0D0A09202020203C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D7061676522202F3E0D0A093C2F756C3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765223E0D0A093C6C693E0D0A09093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B6368696C642D706167652D69647D22207461726765743D225F746F70223E0D0A0909093C623E3C78736C3A76616C75652D6F662073656C6563743D226368696C642D706167652D6E616D6522202F3E3C2F623E0D0A09093C2F613E3C62722F3E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226368696C642D706167652D6465736372697074696F6E22202F3E3C62722F3E0D0A093C2F6C693E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C2F78736C3A7374796C6573686565743E),
	(9006, 'Rubrique Liste de pages filles - Image', 'portlet_childpages_image.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A0D0A3C78736C3A706172616D206E616D653D22736974652D70617468222073656C6563743D22736974652D7061746822202F3E0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706F72746C6574223E0D0A0D0A093C78736C3A7661726961626C65206E616D653D226465766963655F636C617373223E0D0A093C78736C3A63686F6F73653E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D736D616C6C2D646576696365293D273027223E68696464656E2D70686F6E653C2F78736C3A7768656E3E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D6E6F726D616C2D646576696365293D273027223E68696464656E2D7461626C65743C2F78736C3A7768656E3E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D6C617267652D646576696365293D273027223E68696464656E2D6465736B746F703C2F78736C3A7768656E3E0D0A09093C78736C3A6F74686572776973653E3C2F78736C3A6F74686572776973653E0D0A093C2F78736C3A63686F6F73653E0D0A093C2F78736C3A7661726961626C653E0D0A0D0A093C64697620636C6173733D22706F72746C6574207B246465766963655F636C6173737D223E0D0A09093C78736C3A696620746573743D226E6F7428737472696E6728646973706C61792D706F72746C65742D7469746C65293D27312729223E0D0A0909093C68333E0D0A090909093C78736C3A76616C75652D6F662064697361626C652D6F75747075742D6573636170696E673D22796573222073656C6563743D22706F72746C65742D6E616D6522202F3E0D0A0909093C2F68333E0D0A09093C2F78736C3A69663E0D0A09093C78736C3A696620746573743D226E6F7428737472696E6728646973706C61792D706F72746C65742D7469746C65293D27312729223E0D0A0909093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D706F72746C657422202F3E0D0A0909093C78736C3A746578742064697361626C652D6F75747075742D6573636170696E673D22796573223E0D0A09090909093C215B43444154415B3C64697620636C6173733D22636C656172666978223E26233136303B3C2F6469763E5D5D3E0D0A090909093C2F78736C3A746578743E0D0A09093C2F78736C3A69663E0D0A09093C78736C3A696620746573743D22737472696E6728646973706C61792D706F72746C65742D7469746C65293D273127223E0D0A090909093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D70616765732D706F72746C657422202F3E0D0A090909093C78736C3A746578742064697361626C652D6F75747075742D6573636170696E673D22796573223E0D0A09090909093C215B43444154415B3C64697620636C6173733D22636C656172666978223E26233136303B3C2F6469763E5D5D3E0D0A090909093C2F78736C3A746578743E0D0A09093C2F78736C3A69663E0D0A093C2F6469763E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765732D706F72746C6574223E0D0A093C756C20636C6173733D22756E7374796C6564223E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D7061676522202F3E0D0A093C2F756C3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D70616765223E0D0A093C6C693E0D0A2009093C6120687265663D227B24736974652D706174687D3F706167655F69643D7B6368696C642D706167652D69647D22207461726765743D225F746F70223E0D0A09093C78736C3A6170706C792D74656D706C617465732073656C6563743D226368696C642D706167652D696D61676522202F3E0D0A0909093C7374726F6E673E3C78736C3A76616C75652D6F662073656C6563743D226368696C642D706167652D6E616D6522202F3E3C2F7374726F6E673E0D0A09093C2F613E0D0A09093C6272202F3E0D0A09093C78736C3A76616C75652D6F662073656C6563743D226368696C642D706167652D6465736372697074696F6E22202F3E0D0A093C2F6C693E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C212D2D20466F726D617420696D61676520706F6C61726F6964202D2D3E0D0A3C78736C3A74656D706C617465206D617463683D226368696C642D706167652D696D616765223E0D0A202020203C64697620636C6173733D22696D672D706F6C61726F6964207370616E33223E0D0A202020202020203C696D67207372633D227B2E7D2220616C743D227B2E2E2F6368696C642D706167652D6E616D657D22202F3E0D0A202020203C2F6469763E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A0D0A3C2F78736C3A7374796C6573686565743E),
	(10, 'Rubrique HTML - Défaut', 'portlet_html.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A3C78736C3A6F7574707574206D6574686F643D2268746D6C2220696E64656E743D22796573222F3E0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706F72746C6574223E0D0A3C78736C3A7661726961626C65206E616D653D226465766963655F636C617373223E0D0A3C78736C3A63686F6F73653E0D0A093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D736D616C6C2D646576696365293D273027223E68696464656E2D70686F6E653C2F78736C3A7768656E3E0D0A093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D6E6F726D616C2D646576696365293D273027223E68696464656E2D7461626C65743C2F78736C3A7768656E3E0D0A093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D6C617267652D646576696365293D273027223E68696464656E2D6465736B746F703C2F78736C3A7768656E3E0D0A093C78736C3A6F74686572776973653E3C2F78736C3A6F74686572776973653E0D0A3C2F78736C3A63686F6F73653E0D0A3C2F78736C3A7661726961626C653E0D0A0D0A093C64697620636C6173733D22706F72746C6574207B246465766963655F636C6173737D223E0D0A093C78736C3A63686F6F73653E0D0A093C78736C3A7768656E20746573743D226E6F7428737472696E6728646973706C61792D706F72746C65742D7469746C65293D27312729223E0D0A093C68333E3C78736C3A76616C75652D6F662064697361626C652D6F75747075742D6573636170696E673D22796573222073656C6563743D22706F72746C65742D6E616D6522202F3E3C2F68333E0D0A093C78736C3A6170706C792D74656D706C617465732073656C6563743D2268746D6C2D706F72746C657422202F3E0D0A093C2F78736C3A7768656E3E0D0A093C78736C3A6F74686572776973653E0D0A093C78736C3A6170706C792D74656D706C617465732073656C6563743D2268746D6C2D706F72746C657422202F3E0D0A093C2F78736C3A6F74686572776973653E0D0A3C2F78736C3A63686F6F73653E0D0A3C2F6469763E0D0A3C2F78736C3A74656D706C6174653E0D0A090D0A3C78736C3A74656D706C617465206D617463683D2268746D6C2D706F72746C6574223E0D0A093C78736C3A6170706C792D74656D706C617465732073656C6563743D2268746D6C2D706F72746C65742D636F6E74656E7422202F3E0D0A3C2F78736C3A74656D706C6174653E0D0A090D0A3C78736C3A74656D706C617465206D617463683D2268746D6C2D706F72746C65742D636F6E74656E74223E0D0A093C78736C3A76616C75652D6F662064697361626C652D6F75747075742D6573636170696E673D22796573222073656C6563743D222E22202F3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C2F78736C3A7374796C6573686565743E0D0A0D0A0D0A0D0A0D0A),
	(285, 'Rubrique HTML - Fond coloré', 'portlet_html_background.xsl', _binary 0x3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C78736C3A7374796C6573686565742076657273696F6E3D22312E302220786D6C6E733A78736C3D22687474703A2F2F7777772E77332E6F72672F313939392F58534C2F5472616E73666F726D223E0D0A0D0A3C78736C3A6F7574707574206D6574686F643D2268746D6C2220696E64656E743D22796573222F3E0D0A0D0A3C78736C3A74656D706C617465206D617463683D22706F72746C6574223E0D0A0D0A093C78736C3A7661726961626C65206E616D653D226465766963655F636C617373223E0D0A093C78736C3A63686F6F73653E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D736D616C6C2D646576696365293D273027223E68696464656E2D70686F6E653C2F78736C3A7768656E3E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D6E6F726D616C2D646576696365293D273027223E68696464656E2D7461626C65743C2F78736C3A7768656E3E0D0A09093C78736C3A7768656E20746573743D22737472696E6728646973706C61792D6F6E2D6C617267652D646576696365293D273027223E68696464656E2D6465736B746F703C2F78736C3A7768656E3E0D0A09093C78736C3A6F74686572776973653E3C2F78736C3A6F74686572776973653E0D0A093C2F78736C3A63686F6F73653E0D0A093C2F78736C3A7661726961626C653E0D0A090D0A093C64697620636C6173733D22706F72746C6574207B246465766963655F636C6173737D223E0D0A09093C64697620636C6173733D2277656C6C223E0D0A09093C78736C3A63686F6F73653E0D0A0909093C78736C3A7768656E20746573743D226E6F7428737472696E6728646973706C61792D706F72746C65742D7469746C65293D27312729223E0D0A090909093C68323E0D0A09090909093C78736C3A76616C75652D6F662064697361626C652D6F75747075742D6573636170696E673D22796573222073656C6563743D22706F72746C65742D6E616D6522202F3E0D0A090909093C2F68323E0D0A090909093C64697620636C6173733D22706F72746C65742D6261636B67726F756E642D636F6E74656E74202D6C75746563652D626F726465722D7261646975732D626F74746F6D223E0D0A09090909093C78736C3A6170706C792D74656D706C617465732073656C6563743D2268746D6C2D706F72746C657422202F3E0D0A090909093C2F6469763E0D0A0909093C2F78736C3A7768656E3E0D0A0909093C78736C3A6F74686572776973653E0D0A090909093C64697620636C6173733D22706F72746C65742D6261636B67726F756E642D636F6E74656E74202D6C75746563652D626F726465722D726164697573223E0D0A09090909093C78736C3A6170706C792D74656D706C617465732073656C6563743D2268746D6C2D706F72746C657422202F3E0D0A090909093C2F6469763E0D0A0909093C2F78736C3A6F74686572776973653E0D0A09093C2F78736C3A63686F6F73653E0D0A09093C2F6469763E0D0A202020203C2F6469763E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C78736C3A74656D706C617465206D617463683D2268746D6C2D706F72746C6574223E0D0A093C78736C3A6170706C792D74656D706C617465732073656C6563743D2268746D6C2D706F72746C65742D636F6E74656E7422202F3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C78736C3A74656D706C617465206D617463683D2268746D6C2D706F72746C65742D636F6E74656E74223E0D0A093C78736C3A76616C75652D6F662064697361626C652D6F75747075742D6573636170696E673D22796573222073656C6563743D222E22202F3E0D0A3C2F78736C3A74656D706C6174653E0D0A0D0A3C2F78736C3A7374796C6573686565743E);
/*!40000 ALTER TABLE `core_stylesheet` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_style_mode_stylesheet
DROP TABLE IF EXISTS `core_style_mode_stylesheet`;
CREATE TABLE IF NOT EXISTS `core_style_mode_stylesheet` (
  `id_style` int(11) NOT NULL DEFAULT '0',
  `id_mode` int(11) NOT NULL DEFAULT '0',
  `id_stylesheet` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_style`,`id_mode`,`id_stylesheet`),
  KEY `index_style_mode_stylesheet` (`id_stylesheet`,`id_mode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_style_mode_stylesheet: 10 rows
/*!40000 ALTER TABLE `core_style_mode_stylesheet` DISABLE KEYS */;
INSERT INTO `core_style_mode_stylesheet` (`id_style`, `id_mode`, `id_stylesheet`) VALUES
	(3, 0, 211),
	(4, 0, 213),
	(5, 0, 215),
	(6, 0, 217),
	(7, 0, 253),
	(8, 1, 279),
	(100, 0, 10),
	(101, 0, 285),
	(300, 0, 30),
	(301, 0, 9006);
/*!40000 ALTER TABLE `core_style_mode_stylesheet` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_template
DROP TABLE IF EXISTS `core_template`;
CREATE TABLE IF NOT EXISTS `core_template` (
  `template_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `template_value` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`template_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_template: 5 rows
/*!40000 ALTER TABLE `core_template` DISABLE KEYS */;
INSERT INTO `core_template` (`template_name`, `template_value`) VALUES
	('core_first_alert_mail', 'Bonjour ${first_name} ! Votre compte utilisateur arrive à expiration. Pour prolonger sa validité, veuillez <a href="${url}">cliquer ici</a>.</br>Si vous ne le faites pas avant le ${date_valid}, il sera désactivé.'),
	('core_expiration_mail', 'Bonjour ${first_name} ! Votre compte a expiré. Vous ne pourrez plus vous connecter avec, et les données vous concernant ont été anonymisées'),
	('core_other_alert_mail', 'Bonjour ${first_name} ! Votre compte utilisateur arrive à expiration. Pour prolonger sa validité, veuillez <a href="${url}">cliquer ici</a>.</br>Si vous ne le faites pas avant le ${date_valid}, il sera désactivé.'),
	('core_account_reactivated_mail', 'Bonjour ${first_name} ! Votre compte utilisateur a bien été réactivé. Il est désormais valable jusqu\'au ${date_valid}.'),
	('core_password_expired', 'Bonjour ! Votre mot de passe a expiré. Lors de votre prochaine connection, vous pourrez le changer.');
/*!40000 ALTER TABLE `core_template` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_text_editor
DROP TABLE IF EXISTS `core_text_editor`;
CREATE TABLE IF NOT EXISTS `core_text_editor` (
  `editor_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `editor_description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `backOffice` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`editor_name`,`backOffice`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_text_editor: 4 rows
/*!40000 ALTER TABLE `core_text_editor` DISABLE KEYS */;
INSERT INTO `core_text_editor` (`editor_name`, `editor_description`, `backOffice`) VALUES
	('tinymce', 'portal.globalmanagement.editors.labelBackTinyMCE', 1),
	('', 'portal.globalmanagement.editors.labelBackNoEditor', 1),
	('', 'portal.globalmanagement.editors.labelFrontNoEditor', 0),
	('markitupbbcode', 'portal.globalmanagement.editors.labelFrontMarkitupBBCode', 0);
/*!40000 ALTER TABLE `core_text_editor` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_user_parameter
DROP TABLE IF EXISTS `core_user_parameter`;
CREATE TABLE IF NOT EXISTS `core_user_parameter` (
  `parameter_key` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `parameter_value` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`parameter_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_user_parameter: 34 rows
/*!40000 ALTER TABLE `core_user_parameter` DISABLE KEYS */;
INSERT INTO `core_user_parameter` (`parameter_key`, `parameter_value`) VALUES
	('password_duration', '120'),
	('enable_password_encryption', 'false'),
	('encryption_algorithm', ''),
	('default_user_level', '0'),
	('default_user_notification', '1'),
	('default_user_language', 'fr'),
	('default_user_status', '0'),
	('email_pattern', '^[\\w_.\\-!\\#\\$\\%\\&\\\'\\*\\+\\/\\=\\?\\^\\`\\}\\{\\|\\~]+@[\\w_.\\-]+\\.[\\w]+$'),
	('email_pattern_verify_by', ''),
	('force_change_password_reinit', 'false'),
	('password_minimum_length', '8'),
	('password_format', 'false'),
	('password_history_size', ''),
	('maximum_number_password_change', ''),
	('tsw_size_password_change', ''),
	('use_advanced_security_parameters', ''),
	('account_life_time', '12'),
	('time_before_alert_account', '30'),
	('nb_alert_account', '2'),
	('time_between_alerts_account', '10'),
	('access_failures_max', '3'),
	('access_failures_interval', '10'),
	('expired_alert_mail_sender', 'lutece@nowhere.com'),
	('expired_alert_mail_subject', 'Votre compte a expiré'),
	('first_alert_mail_sender', 'lutece@nowhere.com'),
	('first_alert_mail_subject', 'Votre compte va bientot expirer'),
	('other_alert_mail_sender', 'lutece@nowhere.com'),
	('other_alert_mail_subject', 'Votre compte va bientot expirer'),
	('account_reactivated_mail_sender', 'lutece@nowhere.com'),
	('account_reactivated_mail_subject', 'Votre compte a bien été réactivé'),
	('access_failures_captcha', '1'),
	('notify_user_password_expired', ''),
	('password_expired_mail_sender', 'lutece@nowhere.com'),
	('password_expired_mail_subject', 'Votre mot de passe a expiré');
/*!40000 ALTER TABLE `core_user_parameter` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_user_password_history
DROP TABLE IF EXISTS `core_user_password_history`;
CREATE TABLE IF NOT EXISTS `core_user_password_history` (
  `id_user` int(11) NOT NULL,
  `password` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `date_password_change` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_user`,`date_password_change`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_user_password_history: 0 rows
/*!40000 ALTER TABLE `core_user_password_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_password_history` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_user_preferences
DROP TABLE IF EXISTS `core_user_preferences`;
CREATE TABLE IF NOT EXISTS `core_user_preferences` (
  `id_user` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `pref_key` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `pref_value` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id_user`,`pref_key`),
  KEY `index_user_preferences` (`id_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_user_preferences: 0 rows
/*!40000 ALTER TABLE `core_user_preferences` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_preferences` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_user_right
DROP TABLE IF EXISTS `core_user_right`;
CREATE TABLE IF NOT EXISTS `core_user_right` (
  `id_right` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `id_user` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_right`,`id_user`),
  KEY `index_user_right` (`id_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_user_right: 41 rows
/*!40000 ALTER TABLE `core_user_right` DISABLE KEYS */;
INSERT INTO `core_user_right` (`id_right`, `id_user`) VALUES
	('CONTACT_MANAGEMENT', 1),
	('CORE_ADMIN_SITE', 1),
	('CORE_ADMIN_SITE', 2),
	('CORE_ADMINDASHBOARD_MANAGEMENT', 1),
	('CORE_CACHE_MANAGEMENT', 1),
	('CORE_DAEMONS_MANAGEMENT', 1),
	('CORE_DASHBOARD_MANAGEMENT', 1),
	('CORE_FEATURES_MANAGEMENT', 1),
	('CORE_GLOBAL_MANAGEMENT', 1),
	('CORE_LEVEL_RIGHT_MANAGEMENT', 1),
	('CORE_LINK_SERVICE_MANAGEMENT', 1),
	('CORE_LINK_SERVICE_MANAGEMENT', 2),
	('CORE_LOGS_VISUALISATION', 1),
	('CORE_MAILINGLISTS_MANAGEMENT', 1),
	('CORE_MODES_MANAGEMENT', 1),
	('CORE_PAGE_TEMPLATE_MANAGEMENT', 1),
	('CORE_PAGE_TEMPLATE_MANAGEMENT', 2),
	('CORE_PLUGINS_MANAGEMENT', 1),
	('CORE_PROPERTIES_MANAGEMENT', 1),
	('CORE_PROPERTIES_MANAGEMENT', 2),
	('CORE_RBAC_MANAGEMENT', 1),
	('CORE_RIGHT_MANAGEMENT', 1),
	('CORE_ROLES_MANAGEMENT', 1),
	('CORE_ROLES_MANAGEMENT', 2),
	('CORE_SEARCH_INDEXATION', 1),
	('CORE_SEARCH_INDEXATION', 2),
	('CORE_SEARCH_MANAGEMENT', 1),
	('CORE_SEARCH_MANAGEMENT', 2),
	('CORE_STYLES_MANAGEMENT', 1),
	('CORE_STYLESHEET_MANAGEMENT', 1),
	('CORE_USERS_MANAGEMENT', 1),
	('CORE_USERS_MANAGEMENT', 2),
	('CORE_WORKGROUPS_MANAGEMENT', 1),
	('CORE_WORKGROUPS_MANAGEMENT', 2),
	('CORE_XSL_EXPORT_MANAGEMENT', 1),
	('MANAGE_OPENGRAPH_SOCIALHUB', 1),
	('RESOURCE_EXTENDER_MANAGEMENT', 1),
	('SEARCH_STATS_MANAGEMENT', 1),
	('SEO_MANAGEMENT', 1),
	('SYSTEMINFO_MANAGEMENT', 1),
	('THEME_MANAGEMENT', 1);
/*!40000 ALTER TABLE `core_user_right` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_user_role
DROP TABLE IF EXISTS `core_user_role`;
CREATE TABLE IF NOT EXISTS `core_user_role` (
  `role_key` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `id_user` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`role_key`,`id_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_user_role: 9 rows
/*!40000 ALTER TABLE `core_user_role` DISABLE KEYS */;
INSERT INTO `core_user_role` (`role_key`, `id_user`) VALUES
	('all_site_manager', 1),
	('all_site_manager', 2),
	('extend_manager', 1),
	('extend_manager', 2),
	('extend_opengraph_manager', 1),
	('extend_opengraph_manager', 2),
	('super_admin', 1),
	('super_admin', 2),
	('theme_manager', 1);
/*!40000 ALTER TABLE `core_user_role` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.core_xsl_export
DROP TABLE IF EXISTS `core_xsl_export`;
CREATE TABLE IF NOT EXISTS `core_xsl_export` (
  `id_xsl_export` int(11) NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `extension` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id_file` int(11) DEFAULT NULL,
  `plugin` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  PRIMARY KEY (`id_xsl_export`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.core_xsl_export: 2 rows
/*!40000 ALTER TABLE `core_xsl_export` DISABLE KEYS */;
INSERT INTO `core_xsl_export` (`id_xsl_export`, `title`, `description`, `extension`, `id_file`, `plugin`) VALUES
	(125, 'Coeur - Export CSV des administrateurs', 'Export des utilisateurs back office dans un fichier CSV', 'csv', 125, 'core'),
	(126, 'Coeur - Export XML des administrateurs', 'Export des utilisateurs back office dans un fichier XML', 'xml', 126, 'core');
/*!40000 ALTER TABLE `core_xsl_export` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_comment
DROP TABLE IF EXISTS `extend_comment`;
CREATE TABLE IF NOT EXISTS `extend_comment` (
  `id_comment` int(11) NOT NULL DEFAULT '0',
  `id_resource` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `resource_type` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `date_comment` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ip_address` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `comment` mediumtext COLLATE utf8_unicode_ci NOT NULL,
  `is_published` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_comment`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_comment: 0 rows
/*!40000 ALTER TABLE `extend_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `extend_comment` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_comment_config
DROP TABLE IF EXISTS `extend_comment_config`;
CREATE TABLE IF NOT EXISTS `extend_comment_config` (
  `id_extender` int(11) NOT NULL DEFAULT '0',
  `is_moderated` smallint(6) NOT NULL DEFAULT '0',
  `nb_comments` int(11) NOT NULL DEFAULT '1',
  `id_mailing_list` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_extender`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_comment_config: 1 rows
/*!40000 ALTER TABLE `extend_comment_config` DISABLE KEYS */;
INSERT INTO `extend_comment_config` (`id_extender`, `is_moderated`, `nb_comments`, `id_mailing_list`) VALUES
	(-1, 1, 1, -1);
/*!40000 ALTER TABLE `extend_comment_config` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_default_extendable_resource
DROP TABLE IF EXISTS `extend_default_extendable_resource`;
CREATE TABLE IF NOT EXISTS `extend_default_extendable_resource` (
  `id_resource` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `resource_type` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_default_extendable_resource: 0 rows
/*!40000 ALTER TABLE `extend_default_extendable_resource` DISABLE KEYS */;
/*!40000 ALTER TABLE `extend_default_extendable_resource` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_extender_hit
DROP TABLE IF EXISTS `extend_extender_hit`;
CREATE TABLE IF NOT EXISTS `extend_extender_hit` (
  `id_hit` int(11) NOT NULL DEFAULT '0',
  `id_resource` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `resource_type` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `nb_hits` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_hit`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_extender_hit: 0 rows
/*!40000 ALTER TABLE `extend_extender_hit` DISABLE KEYS */;
/*!40000 ALTER TABLE `extend_extender_hit` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_feedback_config
DROP TABLE IF EXISTS `extend_feedback_config`;
CREATE TABLE IF NOT EXISTS `extend_feedback_config` (
  `id_extender` int(11) NOT NULL DEFAULT '0',
  `message` mediumtext COLLATE utf8_unicode_ci NOT NULL,
  `id_mailing_list` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_extender`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_feedback_config: 1 rows
/*!40000 ALTER TABLE `extend_feedback_config` DISABLE KEYS */;
INSERT INTO `extend_feedback_config` (`id_extender`, `message`, `id_mailing_list`) VALUES
	(-1, 'Vous avez une remarque à faire, une expérience à raconter sur le contenu de la page ou sur le service dont il est question ?', 1);
/*!40000 ALTER TABLE `extend_feedback_config` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_opengraph_config
DROP TABLE IF EXISTS `extend_opengraph_config`;
CREATE TABLE IF NOT EXISTS `extend_opengraph_config` (
  `id_extender` int(11) NOT NULL,
  `id_socialhub` int(11) NOT NULL,
  PRIMARY KEY (`id_extender`,`id_socialhub`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_opengraph_config: 0 rows
/*!40000 ALTER TABLE `extend_opengraph_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `extend_opengraph_config` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_opengraph_socialhub
DROP TABLE IF EXISTS `extend_opengraph_socialhub`;
CREATE TABLE IF NOT EXISTS `extend_opengraph_socialhub` (
  `opengraph_socialhub_id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `content_header` mediumtext COLLATE utf8_unicode_ci,
  `content_body` mediumtext COLLATE utf8_unicode_ci NOT NULL,
  `content_footer` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`opengraph_socialhub_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_opengraph_socialhub: 3 rows
/*!40000 ALTER TABLE `extend_opengraph_socialhub` DISABLE KEYS */;
INSERT INTO `extend_opengraph_socialhub` (`opengraph_socialhub_id`, `name`, `content_header`, `content_body`, `content_footer`) VALUES
	(1, 'facebook', '', '<div id="fb-root"></div>\n<div class="fb-like" data-send="false" data-width="30" data-layout="button_count" data-show-faces="false" data-font="arial"></div>', '<script type="text/javascript">// <![CDATA[\n(function(d, s, id) {\nvar js, fjs = d.getElementsByTagName(s)[0];\nif (d.getElementById(id)) return;\njs = d.createElement(s); js.id = id;\njs.src = "//connect.facebook.net/fr_FR/all.js#xfbml=1";\nfjs.parentNode.insertBefore(js, fjs);\n}(document, \'script\', \'facebook-jssdk\'));\n// ]]></script>\n'),
	(2, 'Google+', '', '<div class="g-plusone" data-size="medium" data-annotation="none"></div>', '<script type="text/javascript">\nwindow.___gcfg = {lang: \'fr\'};\n(function() {\nvar po = document.createElement(\'script\'); po.type = \'text/javascript\'; po.async = true;\npo.src = \'https://apis.google.com/js/plusone.js\';\nvar s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(po, s);\n})();\n</script>\n'),
	(3, 'Tweeter', '', '<a href="https://twitter.com/share" class="twitter-share-button" data-lang="fr" data-count="none">Tweeter</a>\n<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>', '');
/*!40000 ALTER TABLE `extend_opengraph_socialhub` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_resource_extender
DROP TABLE IF EXISTS `extend_resource_extender`;
CREATE TABLE IF NOT EXISTS `extend_resource_extender` (
  `id_extender` int(11) NOT NULL DEFAULT '0',
  `extender_type` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `id_resource` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `resource_type` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id_extender`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_resource_extender: 0 rows
/*!40000 ALTER TABLE `extend_resource_extender` DISABLE KEYS */;
/*!40000 ALTER TABLE `extend_resource_extender` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.extend_resource_extender_history
DROP TABLE IF EXISTS `extend_resource_extender_history`;
CREATE TABLE IF NOT EXISTS `extend_resource_extender_history` (
  `id_history` bigint(20) NOT NULL DEFAULT '0',
  `extender_type` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `id_resource` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `resource_type` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `user_guid` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `ip_address` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_history`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.extend_resource_extender_history: 0 rows
/*!40000 ALTER TABLE `extend_resource_extender_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `extend_resource_extender_history` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.html_portlet
DROP TABLE IF EXISTS `html_portlet`;
CREATE TABLE IF NOT EXISTS `html_portlet` (
  `id_portlet` int(11) NOT NULL DEFAULT '0',
  `html` mediumtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id_portlet`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.html_portlet: 13 rows
/*!40000 ALTER TABLE `html_portlet` DISABLE KEYS */;
INSERT INTO `html_portlet` (`id_portlet`, `html`) VALUES
	(55, '<p>Lutece est un moteur de portail libre qui permet de créer des\r\nsites internet/intranet avec des fonctions de gestion de contenu\r\navancées. Il constitue également un cadre de développement\r\nd\'applications métiers ayant des composantes BackOffice/Front\r\nOffice et pouvant s\'intégrer de manière modulaire dans un\r\nportail.</p>\r\n<p>Cette plate-forme est utilisée par de grands sites français\r\nnotamment dans le milieu des collectivités locales.</p>\r\n<p>&#160;</p>\r\n'),
	(98, '<ul>\r\n  <li>Les interfaces utilisateur du Front Office (le site) et du\r\n  back Office (l\'administration du site) sont " \r\n  <strong>Responsive Design</strong>" : c\'est à dire qu\'elles\r\n  s\'adaptent au type de terminal (smartphone, tablette, PC, ...) à\r\n  partir duquel elles sont consultées. Le même site peut donc être\r\n  désormais vu de manière optimale sur un mobile et sur un grand\r\n  écran.</li>\r\n  <li>La \r\n  <strong>personnalisation des thèmes</strong> est simplifiée grâce\r\n  au framework Bootstrap et à la technologie LESS. Des thèmes\r\n  gratuits et prêts à l\'emploi sont disponibles sur des sites tels\r\n  que \r\n  <a title="Lien externe vers le site Bootswatch"\r\n  href="http://bootswatch.com/"\r\n  target="_blank">Bootswatch</a>.</li>\r\n  <li>Amélioration des fonctions \r\n  <strong>SEO</strong> pour optimiser le référencement des sites et\r\n  l\'indexation par les moteurs de recherche : "Friendly URL",\r\n  Sitemap, URL canoniques, etc... . Les URL techniques peuvent par\r\n  exemple être remplacées par des URL explicites ayant une\r\n  extension ".html" à l\'image d\'un site statique.</li>\r\n  <li>\r\n  <strong>Extensions fonctionnelles</strong> (commentaires, votes,\r\n  notations, partage sur les réseaux sociaux ...) dorénavant\r\n  pluggables sur tous les types de contenus (pages, articles,\r\n  ...)</li>\r\n</ul>\r\n<p>&#160;</p>\r\n'),
	(57, '<div class="portlet-content portlet-content">\r\n  <h3>Organisation du portail</h3>\r\n  <ul>\r\n    <li>Un site conçu à partir de Lutèce se présente sous la forme\r\n    d\'une arborescence dynamique de pages, dont la racine est la\r\n    page d\'accueil.</li>\r\n    <li>L\'information présentée dans chacune des pages du portail\r\n    s\'organise à l\'intérieur de blocs appelés rubriques de page.\r\n    Ces rubriques de page constituent des zones de texte qui vont\r\n    pouvoir être placées dynamiquement à l\'intérieur d\'une page par\r\n    le webmestre au moment de la conception et de la mise à jour\r\n    des pages. Chaque page est associée à un modèle de composition\r\n    composé de lignes et de colonnes.</li>\r\n    <li>Les données techniques relatives à l\'organisation d\'un site\r\n    (pages, rubriques, types de contenu, feuilles de style,... )\r\n    sont stockées en base de données.</li>\r\n  </ul>\r\n  <br />\r\n  <h3>Navigation</h3>\r\n  <ul>\r\n    <li>Les pages principales du site sont regroupées dans une\r\n    barre de navigation toujours visible.</li>\r\n    <li>L\'accès direct aux pages intérieures se fait à partir de\r\n    menus déroulants associés à chacune des pages principales du\r\n    site.</li>\r\n    <li>Un chemin de navigation interactif est présent sur chacune\r\n    des pages visitées</li>\r\n    <li>La navigation dans l\'arborescence du site se fait également\r\n    à partir de liens placés directement dans les pages (liens vers\r\n    les pages filles).</li>\r\n    <li>Le plan du site, généré dynamiquement, permet l\'accès\r\n    direct aux pages du site</li>\r\n  </ul>\r\n  <br />\r\n  <h3>Services</h3>\r\n  <ul>\r\n    <li>La gestion d\'un ensemble de services est assurée par des\r\n    pages spéciales, toujours visibles (moteur de recherche, plan\r\n    du site, forum, chat, lettres d\'information, contacts, liens\r\n    vers d\'autres sites Internet).</li>\r\n    <li>Certains produits logiciels disponibles en « Open Source »\r\n    ont été intégrés sous la forme de services (indexation\r\n    full-text et moteur de recherche, forum modéré).</li>\r\n    <li>Rubriques de page et types de contenu</li>\r\n    <li>Les rubriques de page, dans lesquelles vont se placer le\r\n    contenu web, ont des types prédéfinis, déterminés par le type\r\n    de contenu lui-même. Les types de rubriques disponibles sont :\r\n    Liste d\'articles (actualités, agenda, ...), fiche de\r\n    renseignements, texte libre ou HTML, document au format XML,\r\n    liste de personnes, fichiers à télécharger, liste de liens\r\n    Internet, liste de liens pour la navigation intérieure,\r\n    syndication de contenu externe (au format RSS).</li>\r\n    <li>Le placement de ces rubriques dans une page suit le modèle\r\n    de composition de la page, qui s\'organise en lignes et en\r\n    colonnes.</li>\r\n    <li>Séparation entre contenu et présentation</li>\r\n    <li>La séparation entre le contenu et la mise en forme est\r\n    rendue possible par le choix du format d\'échange XML, dans\r\n    lequel sont traduites les informations structurées issues de la\r\n    base de données.</li>\r\n    <li>L\'affichage dynamique du contenu des pages est assuré par\r\n    la transformation XSLT du contenu XML généré et des feuilles de\r\n    style XSL associées à chacune des rubriques.</li>\r\n    <li>Des modèles de mise en page de contenu sont définis pour\r\n    chaque type de rubrique et peuvent être complétés au fur et à\r\n    mesure des besoins.</li>\r\n    <li>Tant que le contenu d\'une page n\'est pas modifié, celle-ci\r\n    n\'est pas recalculée (gestion intégrée du cache).</li>\r\n  </ul>\r\n  <br />\r\n  <h3>Outil d\'administration pour la mise en page des\r\n  rubriques</h3>\r\n  <ul>\r\n    <li>l\'outil d\'administration du portail est destiné aux\r\n    webmestres et aux assistants de publication.</li>\r\n    <li>Cet outil a été conçu pour être simple à utiliser, et\r\n    n\'exige pas d\'avoir de compétences techniques spéciales.</li>\r\n    <li>Un ensemble d\'interfaces graphiques assiste le webmestre\r\n    dans la création des pages, le choix des rubriques, la saisie\r\n    ou la publication de contenus, le choix du style de\r\n    présentation.</li>\r\n    <li>Une fenêtre de prévisualisation permet au webmestre\r\n    d\'afficher la page sur laquelle il travaille et d\'agir\r\n    directement sur son contenu.</li>\r\n    <li>La construction des pages du portail et la mise à jour des\r\n    contenus se font dans un environnement de pré-production.</li>\r\n    <li>La mise en ligne des ajouts ou modifications apportées en\r\n    pré-production se fait après validation du webmestre.</li>\r\n  </ul>\r\n  <br />\r\n  <h3>Outils d\'administration des services</h3>\r\n  <ul>\r\n    <li>Le webmestre dispose d\'une interface graphique pour animer\r\n    et modérer les groupes de discussion du portail (produit Open\r\n    Source Jive).</li>\r\n    <li>Le webmestre peut créer une ou plusieurs lettres\r\n    d\'information thématiques, associées chacune à un ou plusieurs\r\n    thèmes d\'articles. Le contenu d\'une lettre est généré à partir\r\n    de la liste d\'articles publiés sur les thèmes choisis dans les\r\n    rubriques du portail depuis le dernier envoi. L\'envoi d\'une\r\n    lettre est déclenché par l\'action du webmestre.</li>\r\n    <li>La liste des personnes à contacter depuis le portail est\r\n    également géré depuis l\'outil d\'administration.</li>\r\n    <li>Outil de création de comptes utilisateurs</li>\r\n    <li>Un profil « administrateur » permet de créer les comptes de\r\n    webmestres et de contributeurs externes.</li>\r\n    <li>Le profil « webmestre » permet de créer l\'ensemble des\r\n    comptes utilisateurs amenés à produire du contenu ou à\r\n    l\'assister dans la publication.</li>\r\n    <li>Chaque compte utilisateur est rattaché à un compte de\r\n    fournisseurs de contenu, auquel est attribué un ou plusieurs\r\n    flux d\'information. Le flux d\'information sert à définir un\r\n    contexte propre à chaque fournisseur (portée de l\'information,\r\n    type et origine de l\'information).</li>\r\n  </ul>\r\n  <br />\r\n  <h3>Outil de production de contenu</h3>\r\n  <ul>\r\n    <li>Les outils de production de contenu sont destinés aux\r\n    webmestres et aux différents contributeurs externes.</li>\r\n    <li>La production de contenu consiste en la saisie d\'articles\r\n    ou de fiches de renseignement, à l\'aide d\'un éditeur de texte\r\n    intégré. Une image peut être associée à chaque contenu\r\n    produit.</li>\r\n    <li>Les contenus sont produits sans indication de leur mise en\r\n    page future (principe de la séparation entre contenu et mise en\r\n    forme).</li>\r\n    <li>Une bibliothèque d\'images permet au webmestre de charger et\r\n    de stocker les images qu\'il souhaite placer dans les rubriques\r\n    de texte de son portail.</li>\r\n  </ul>\r\n  <br />\r\n  <h3>Outil de publication de contenu</h3>\r\n  <ul>\r\n    <li\r\n    style="list-style-type: none; list-style-image: none; list-style-position: outside;">­</li>\r\n    <li>L\'outil de publication de contenus web dans les pages du\r\n    site est destiné au webmestre et aux assistants de publication.\r\n    Cet outil permet de mettre à la disposition du webmestre\r\n    l\'ensemble des contenus produits par les contributeurs et de\r\n    lui en donner un aperçu avant qu\'il ne les place lui-même dans\r\n    son portail.</li>\r\n    <li>La publication consiste à associer un article à une ou\r\n    plusieurs rubriques de page destinées à recevoir ce type de\r\n    contenu (liste d\'articles ou fiche de renseignements).</li>\r\n    <li>Un article peut être publié à plusieurs endroits du site,\r\n    et se présenter sous différentes formes (titre seulement ;\r\n    titre, image et résumé ; titre, dates de début et de fin)</li>\r\n    <li>La validité d\'un article est gérée au niveau de ses\r\n    propriétés et conditionne son affichage.</li>\r\n    <li>Il est possible d\'associer un flux d\'information à une\r\n    rubrique de page, pour rendre automatique la publication des\r\n    contenus produits sur ce flux dans la rubrique.</li>\r\n  </ul>\r\n</div>\r\n'),
	(58, '<p>Plusieurs sources de documentation sont disponibles :</p>\r\n<p>&#160;</p>\r\n<ul>\r\n  <li>\r\n    <a title="Lien externe vers la documentation"\r\n    href="http://dev.lutece.paris.fr/fr/user/lutece_v2_overview.html"\r\n     target="_blank">Un guide utilisateur</a>\r\n  </li>\r\n  <li>\r\n    <a title="Lien externe vers la documentation"\r\n    href="https://dev.lutece.paris.fr/confluence/"\r\n    target="_blank">Un Wiki contenant notamment des tutoriels\r\n    techniques</a>\r\n  </li>\r\n  <li>\r\n    <a title="Lien externe vers la documentation"\r\n    href="http://dev.lutece.paris.fr/fr/tech/standard_development.html"\r\n     target="_blank">Des normes de développement</a>\r\n  </li>\r\n  <li>\r\n    <a title="Lien externe vers la documentation"\r\n    href="http://dev.lutece.paris.fr/fr/tech/developers_resources.html"\r\n     target="_blank">Un guide de développement</a>\r\n  </li>\r\n</ul>\r\n<p>&#160;</p>\r\n<p>&#160;</p>\r\n'),
	(61, 'Le plugin <strong>calendar</strong> permet d\'afficher sur un calendrier à trois vues (jour, semaine, mois) les événements concernant un ou plusieurs agendas simultanément. Les formats supportés pour les agendas sont soit texte, soit iCalendar ( <a href="http://www.ietf.org/rfc/rfc2445.txt" target="_blank" title="Spécifications iCalendar">RFC 2445</a>)<form action="jsp/site/Portal.jsp"><div style="text-align: center;"><input value="calendar" name="page" type="hidden" /><input value="projet1" name="agenda" checked="true" type="checkbox" />Projet 1 (Fichier .ics) <input value="projet2" name="agenda" checked="true" type="checkbox" />Projet2 (Fichier .txt) <input value="Afficher les agendas" name="Submit" type="submit" /></div></form>'),
	(64, '<h3>Normes de développement</h3><p>Le développement sous Lutèce est soumis à un ensemble de règles qui permettent de garantir l\'homogénéité et la maintenabilité du code. L\'ensemble de ces règles est décrit dans le document disponible ci-dessous.</p><h3>API de Lutece</h3><p>Les documentations disponibles sont :</p><ul><li><a target="_blank" href="http://dev.lutece.paris.fr/fr/" title="Guide du développeur">Guide du développeur</a></li><li><a target="_blank" href="http://dev.lutece.paris.fr/lutece-core/fr/apidocs/index.html" title="Javadocs">Javadoc</a></li></ul><h3>Générateur de code</h3><p>Un plugin nommé <a target="_self" href="jsp/site/Portal.jsp?page=codewizard">codewizard</a> vous permet de générer très rapidement certaines parties de code assez fastidieuses : classes métier, DAO et même des classes JUnit.</p><h3>Analyseurs de code</h3><p>Plusieurs outils libres et gratuit, tels que PMD et CheckStyle, permettent de vérifier le respect d\'un certain nombre de règles de l\'art. Vous trouverez ci-dessous les fichiers de configuration pour ces outils et ci contre leurs sites officiels.</p>'),
	(99, '<p>\r\n  <img class="img-rounded"\r\n  src="http://lorempixel.com/200/400/abstract/" alt="" />\r\n</p>\r\n'),
	(66, '<a href="jsp/site/Portal.jsp?page=xmlpage&amp;xmlpage=coverage-core&amp;style=html">Mesure de la couverture des tests unitaires du noyau</a>­'),
	(91, '<form action="jsp/admin/DoAdminLogin.jsp" method="post">\r\n  <h4>&#160;Accès à l\'administration du site</h4>\r\n  <div class="well">\r\n  <p>\r\n    <strong>Choisissez votre profil :</strong>\r\n  </p>\r\n  <div>\r\n  <input id="access_code_admin" title="administrateur" type="radio"\r\n  name="access_code" value="admin" checked="checked" />\r\n &nbsp; Administrateur technique</div>\r\n  <div>\r\n  <input id="access_code_webmaster" title="webmaster" type="radio"\r\n  name="access_code" value="lutece" /> &nbsp; Webmaster - Gestion de\r\n  contenu</div>\r\n  <div>\r\n  <input id="access_code_redac" title="redacteur" type="radio"\r\n  name="access_code" value="redac" /> &nbsp; Rédacteur - Producteur de\r\n  contenu</div>\r\n  <div>\r\n    <input type="hidden" name="password" value="adminadmin" />\r\n  </div>\r\n  <br /> \r\n  <button class="btn btn-primary" type="submit"><i class="icon-user icon-white"></i> &nbsp; Se\r\n  connecter</button></div>\r\n</form>\r\n'),
	(92, '<div id="myCarousel" class="carousel slide">\r\n<div class="carousel-inner">\r\n  <div class="active item">\r\n  <img src="document?id=21" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>Le site de la mairie de Paris</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=14" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>Météo France</p>\r\n    <p>&#160;</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=19" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>Outil de dématérialisation des documents de séance de\r\n    conseil (municipal ou général)</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=12" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>La Mairie de Marseille</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=11" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>Les mairie d\'arrondissement à Paris</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=16" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>Les télé procédures de la ville de Marseille</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=15" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>Eau de Paris</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=13" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>Thalys card</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=17" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>www.notaires.fr</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=9" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>La mairie de Bobigny</p>\r\n  </div></div>\r\n  <div class="item">\r\n  <img src="document?id=20" alt="" /> \r\n  <div class="carousel-caption">\r\n    <p>e-bourgogne</p>\r\n  </div></div>\r\n</div>\r\n<a class="left carousel-control" href="#myCarousel"\r\ndata-slide="prev">‹</a> \r\n<a class="right carousel-control" href="#myCarousel"\r\ndata-slide="next">›</a></div>\r\n'),
	(95, '<h2>Ajouter du contenu dans Lutece</h2><div>Lutece vous permet d\'ajouter du contenu dans vos pages de plusieurs manières : <br /><ol> <li>par un éditeur de texte riche. Vous pouvez éditer vos pages comme si vous étiez dans Word©</li><li>par un éditeur html/css/javascript. Vous pouvez éditer  directement le code source de vos pages.</li></ol><p>Quelle que soit la méthode que vous choisissez, vous avez un fonctionnalité d\'insertion dynamique de contenu (linkservice) qui vous permets d\'ajouter des contenus riches provenant d\'autres sources. Vous pouvez ainsi ajouter : <br /><ol>  <li>des videos YouTube</li> <li>des google maps</li> <li>des liens vers des applications métiers disponibles dans Lutece</li> <li>des medias (pdf, video, images, document) depuis la médiathèque interne à Lutece</li> <li>des galeries d\'images Web 2.0 comme sur la page d\'accueil</li></ol></div><br />'),
	(96, '<p>Le formulaire sur la colonne de gauche est un exemple de formulaire généré en quelques clics par le <a href="http://dev.lutece.paris.fr/plugins/plugin-form/fr/index.html" target="_blank">plugin-form</a>.</p><p>Simples et intuitifs à créer, les formulaires créés avec le <a href="http://dev.lutece.paris.fr/plugins/plugin-form/fr/index.html" target="_blank">plugin-form</a> sont une solution adaptée pour interagir avec vos utilisateurs.</p><p>Configurable, le <a href="http://dev.lutece.paris.fr/plugins/plugin-form/fr/index.html" target="_blank">plugin-form</a> permet de paramétrer ce que voit l\'utilisateur après validation du formulaire. Les résultats du formulaire sous forme d\'histogramme ou de camenbert ?<br />A vous de choisir !</p><p>Les résultats sont ensuite exportables au format Excel et Xml.</p><p>Vous voulez plus d\'interactivité encore ?<br />Peut-être que le <a href="jsp/site/Portal.jsp?page=digg&amp;id_digg=1">plugin-digg</a> ou le <a href="jsp/site/Portal.jsp?page=calendar">plugin-calendar</a> répondront à vos attentes.</p>'),
	(97, '<p>Un plugin nommé <a href="jsp/site/Portal.jsp?page=codewizard">codewizard</a> vous permet de générer très rapidement certaines parties de code assez fastidieuses : classes métier, DAO et même des classes JUnit.</p><br />');
/*!40000 ALTER TABLE `html_portlet` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.searchstats_queries
DROP TABLE IF EXISTS `searchstats_queries`;
CREATE TABLE IF NOT EXISTS `searchstats_queries` (
  `yyyy` int(11) DEFAULT NULL,
  `mm` int(11) DEFAULT NULL,
  `dd` int(11) DEFAULT NULL,
  `hh` int(11) DEFAULT NULL,
  `query` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `results_count` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.searchstats_queries: 0 rows
/*!40000 ALTER TABLE `searchstats_queries` DISABLE KEYS */;
/*!40000 ALTER TABLE `searchstats_queries` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.seo_friendly_url
DROP TABLE IF EXISTS `seo_friendly_url`;
CREATE TABLE IF NOT EXISTS `seo_friendly_url` (
  `id_url` int(11) NOT NULL DEFAULT '0',
  `friendly_url` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `technical_url` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modification` timestamp NOT NULL DEFAULT '2012-10-10 00:00:00',
  `is_canonical` int(11) NOT NULL DEFAULT '0',
  `is_sitemap` int(11) NOT NULL DEFAULT '0',
  `sitemap_lastmod` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `sitemap_changefreq` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `sitemap_priority` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  PRIMARY KEY (`id_url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.seo_friendly_url: 3 rows
/*!40000 ALTER TABLE `seo_friendly_url` DISABLE KEYS */;
INSERT INTO `seo_friendly_url` (`id_url`, `friendly_url`, `technical_url`, `date_creation`, `date_modification`, `is_canonical`, `is_sitemap`, `sitemap_lastmod`, `sitemap_changefreq`, `sitemap_priority`) VALUES
	(1, '/sitemap.html', '/jsp/site/Portal.jsp?page=map', '2013-06-24 11:21:51', '2012-10-10 00:00:00', 1, 1, '2012-10-10', 'monthly', '0.8'),
	(2, '/contacts.html', '/jsp/site/Portal.jsp?page=contact', '2013-06-24 11:21:51', '2012-10-10 00:00:00', 1, 1, '2012-10-10', 'monthly', '0.8'),
	(3, '/credits.html', '/jsp/site/PopupCredits.jsp', '2013-06-24 11:21:51', '2012-10-10 00:00:00', 1, 1, '2012-10-10', 'monthly', '0.8');
/*!40000 ALTER TABLE `seo_friendly_url` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.seo_properties
DROP TABLE IF EXISTS `seo_properties`;
CREATE TABLE IF NOT EXISTS `seo_properties` (
  `property_key` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `property_value` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`property_key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.seo_properties: 0 rows
/*!40000 ALTER TABLE `seo_properties` DISABLE KEYS */;
/*!40000 ALTER TABLE `seo_properties` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.seo_rule
DROP TABLE IF EXISTS `seo_rule`;
CREATE TABLE IF NOT EXISTS `seo_rule` (
  `id_rule` int(11) NOT NULL DEFAULT '0',
  `rule_from` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `rule_to` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id_rule`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.seo_rule: 3 rows
/*!40000 ALTER TABLE `seo_rule` DISABLE KEYS */;
INSERT INTO `seo_rule` (`id_rule`, `rule_from`, `rule_to`) VALUES
	(1, '/page/([0-9]+)', '/jsp/site/Portal.jsp?page_id=$1'),
	(2, '/app/([a-z]+)', '/jsp/site/Portal.jsp?page=$1'),
	(3, '/map', '/jsp/site/Portal.jsp?page=map');
/*!40000 ALTER TABLE `seo_rule` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.theme_global
DROP TABLE IF EXISTS `theme_global`;
CREATE TABLE IF NOT EXISTS `theme_global` (
  `global_theme_code` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`global_theme_code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.theme_global: 1 rows
/*!40000 ALTER TABLE `theme_global` DISABLE KEYS */;
INSERT INTO `theme_global` (`global_theme_code`) VALUES
	('blue');
/*!40000 ALTER TABLE `theme_global` ENABLE KEYS */;


-- Dumping structure for table site-edito-mini.theme_theme
DROP TABLE IF EXISTS `theme_theme`;
CREATE TABLE IF NOT EXISTS `theme_theme` (
  `code_theme` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `theme_description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `path_images` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `path_css` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `theme_author` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `theme_author_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `theme_version` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `theme_licence` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `path_js` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`code_theme`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Dumping data for table site-edito-mini.theme_theme: 5 rows
/*!40000 ALTER TABLE `theme_theme` DISABLE KEYS */;
INSERT INTO `theme_theme` (`code_theme`, `theme_description`, `path_images`, `path_css`, `theme_author`, `theme_author_url`, `theme_version`, `theme_licence`, `path_js`) VALUES
	('amelia', 'Amelia', 'themes/amelia/img/', 'themes/amelia/css', 'bootswatch', 'http://bootswatch.com/', '1.0', 'Apache 2.0', 'js/'),
	('blue', 'Thème Défaut', 'images/', 'css', 'Mairie de Paris', 'http://fr.lutece.paris.fr', '1.0', 'BSD', 'js/'),
	('slate', 'Slate', 'themes/slate/img/', 'themes/slate/css', 'bootswatch', 'http://bootswatch.com/', '1.0', 'Apache 2.0', 'js/'),
	('superhero', 'Superhero', 'themes/superhero/img/', 'themes/superhero/css', 'bootswatch', 'http://bootswatch.com/', '1.0', 'Apache 2.0', 'js/'),
	('united', 'United', 'themes/united/img/', 'themes/united/css', 'bootswatch', 'http://bootswatch.com/', '1.0', 'Apache 2.0', 'js/');
/*!40000 ALTER TABLE `theme_theme` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
