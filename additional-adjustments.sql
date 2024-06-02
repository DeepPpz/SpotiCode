--
-- TOC entry 263 (class 1255 OID 89163)
-- Name: tr_fn_auto_calc_albums_count(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_calc_albums_count() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	IF TG_OP = 'INSERT' THEN
		UPDATE
			artists
		SET
			albums_count = (
				SELECT 
					COUNT(*)
				FROM
					albums
				WHERE 
					album_artist = NEW.album_artist
				)
		WHERE 
			artist_name = NEW.album_artist;
		RETURN NEW;
		
	ELSIF TG_OP = 'DELETE' THEN
		UPDATE
			artists
		SET
			albums_count = (
				SELECT 
					COUNT(*)
				FROM
					albums
				WHERE 
					album_artist = OLD.album_artist
				)
		WHERE 
			artist_name = OLD.album_artist;
		RETURN OLD;

	END IF;
   
END;
$$;


--
-- TOC entry 251 (class 1255 OID 89171)
-- Name: tr_fn_auto_calc_check_all_variables_from_songs(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_calc_check_all_variables_from_songs() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	IF TG_OP = 'INSERT' THEN
		UPDATE
			artists
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					main_artist = NEW.main_artist
				)
		WHERE 
			artist_name = NEW.main_artist;
	
		UPDATE
			music_groups  
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					"group" = NEW."group"
				)
		WHERE 
			group_name = NEW."group";
	
		UPDATE
			genres 
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					genre = NEW.genre
				)
		WHERE 
			genre_name = NEW.genre;
		
		IF EXISTS (
			SELECT 
				1
			FROM 
				songs 
			WHERE 
	        	song_title = NEW.song_title
	        	AND main_artist = NEW. main_artist
		) THEN
			UPDATE
				pending_songs 
			SET
				is_added = TRUE
			WHERE
				song_title = NEW.song_title
	        	AND main_artist = NEW. main_artist;
	    ELSE
	    	UPDATE 
	    		pending_songs 
	    	SET 
	    		is_added = FALSE 
	    	WHERE 
	    		song_title = NEW.song_title
	        	AND main_artist = NEW. main_artist;
		END IF;
		
		RETURN NEW;
		
	ELSIF TG_OP = 'DELETE' THEN
		UPDATE
			artists
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					main_artist = OLD.main_artist
				)
		WHERE 
			artist_name = OLD.main_artist;
	
		UPDATE
			music_groups  
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					"group" = OLD."group"
				)
		WHERE 
			group_name = OLD."group";
		
		UPDATE
			genres 
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					genre = OLD.genre
				)
		WHERE 
			genre_name = OLD.genre;
		
		IF EXISTS (
			SELECT 
				1
			FROM 
				songs 
			WHERE 
	        	song_title = OLD.song_title
	        	AND main_artist = OLD.main_artist
		) THEN
			UPDATE
				pending_songs 
			SET
				is_added = TRUE
			WHERE
				song_title = OLD.song_title
	        	AND main_artist = OLD.main_artist;
	    ELSE
	    	UPDATE 
	    		pending_songs 
	    	SET 
	    		is_added = FALSE 
	    	WHERE 
	    		song_title = OLD.song_title
	        	AND main_artist = OLD. main_artist;
		END IF;
		
		RETURN OLD;
	
	END IF;
   
END;
$$;


--
-- TOC entry 267 (class 1255 OID 89334)
-- Name: tr_fn_auto_calc_on_playlist_songs_count(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_calc_on_playlist_songs_count() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	IF TG_OP = 'INSERT' THEN
		UPDATE
			playlists 
		SET
			songs_local = (
				SELECT 
					COUNT(*)
				FROM
					song_playlist_relations
				WHERE 
					playlist_id = NEW.playlist_id
				)
		WHERE 
			playlist_id = NEW.playlist_id;
		
		UPDATE
			playlists 
		SET
			songs_spotify = (
				SELECT 
					COUNT(*)
				FROM
					song_playlist_relations spr
				JOIN songs s
					ON s.song_id = spr.song_id
				WHERE 
					spr.playlist_id = NEW.playlist_id
					AND s.spotify_link IS NOT NULL
				)
		WHERE 
			playlist_id = NEW.playlist_id;
		
		RETURN NEW;
		
	ELSIF TG_OP = 'DELETE' THEN
		UPDATE
			playlists 
		SET
			songs_local = (
				SELECT 
					COUNT(*)
				FROM
					song_playlist_relations
				WHERE 
					playlist_id = OLD.playlist_id
				)
		WHERE 
			playlist_id = OLD.playlist_id;
		
		UPDATE
			playlists 
		SET
			songs_spotify = (
				SELECT 
					COUNT(*)
				FROM
					song_playlist_relations spr
				JOIN songs s
					ON s.song_id = spr.song_id
				WHERE 
					spr.playlist_id = OLD.playlist_id
					AND s.spotify_link IS NOT NULL
				)
		WHERE 
			playlist_id = OLD.playlist_id;
		
		RETURN OLD;

	END IF;
   
END;
$$;


--
-- TOC entry 250 (class 1255 OID 89165)
-- Name: tr_fn_auto_calc_pending_count(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_calc_pending_count() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	IF TG_OP = 'INSERT' THEN
		UPDATE
			music_groups 
		SET
			pending_count = (
				SELECT 
					COUNT(*)
				FROM
					pending_songs
				WHERE 
					to_group = NEW.to_group
					AND is_added = False
				)
		WHERE 
			group_name = NEW.to_group;
		RETURN NEW;
		
	ELSIF TG_OP = 'DELETE' THEN
		UPDATE
			music_groups
		SET
			pending_count = (
				SELECT 
					COUNT(*)
				FROM
					pending_songs
				WHERE 
					to_group = OLD.to_group
					AND is_added = False
				)
		WHERE 
			group_name = OLD.to_group;
		RETURN OLD;

	END IF;
   
END;
$$;


--
-- TOC entry 266 (class 1255 OID 89339)
-- Name: tr_fn_auto_calc_songs_spotify(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_calc_songs_spotify() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

        UPDATE 
        	playlists 
        SET 
        	songs_spotify = (
            	SELECT 
            		COUNT(*)
            	FROM 
            		song_playlist_relations spr
            	JOIN songs s 
            		ON s.song_id = spr.song_id
            WHERE 
            	spr.playlist_id = playlists.playlist_id
            	AND s.spotify_link IS NOT NULL);

    RETURN NULL;
   
END;
$$;


--
-- TOC entry 265 (class 1255 OID 89167)
-- Name: tr_fn_auto_check_if_artist_exist(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_check_if_artist_exist() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	IF EXISTS (
		SELECT 
			1
		FROM 
			artists 
		WHERE 
        	artist_name = NEW.artist_name
	) THEN
		UPDATE
			pending_songs 
		SET
			new_artist = FALSE
		WHERE
			main_artist = NEW.artist_name;
    ELSE
    	UPDATE 
    		pending_songs 
    	SET 
    		new_artist = TRUE 
    	WHERE 
        	main_artist = NEW.artist_name;
	END IF;
	
	RETURN NEW;
   
END;
$$;


--
-- TOC entry 264 (class 1255 OID 89169)
-- Name: tr_fn_auto_check_new_add_on_pending(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_check_new_add_on_pending() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	IF EXISTS (
		SELECT 
			1
		FROM 
			songs 
		WHERE 
        	song_title = NEW.song_title
        	AND main_artist = NEW. main_artist
	) THEN
		UPDATE
			pending_songs 
		SET
			is_added = TRUE
		WHERE
			song_title = NEW.song_title
        	AND main_artist = NEW. main_artist;
    ELSE
    	UPDATE 
    		pending_songs 
    	SET 
    		is_added = FALSE 
    	WHERE 
    		song_title = NEW.song_title
        	AND main_artist = NEW. main_artist;
	END IF;
	
	IF EXISTS (
			SELECT 
				1
			FROM 
				artists 
			WHERE 
	        	artist_name = NEW.main_artist
		) THEN
			UPDATE
				pending_songs 
			SET
				new_artist = FALSE
			WHERE 
	        	main_artist = NEW.main_artist;
	    ELSE
	    	UPDATE 
	    		pending_songs 
	    	SET 
	    		new_artist = TRUE 
	    	WHERE 
	    		main_artist = NEW.main_artist;
		END IF;
	
	RETURN NEW;

END;
$$;


--
-- TOC entry 248 (class 1255 OID 89159)
-- Name: tr_fn_auto_insert_new_album_to_albums_sites(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_insert_new_album_to_albums_sites() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	INSERT INTO albums_links (album_id)
		VALUES
			(NEW.album_id);
   	RETURN NEW;
   
END;
$$;


--
-- TOC entry 249 (class 1255 OID 89161)
-- Name: tr_fn_auto_insert_new_artist_to_artists_sites(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.tr_fn_auto_insert_new_artist_to_artists_sites() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	INSERT INTO artists_links (artist_id)
		VALUES
			(NEW.artist_id);
   	RETURN NEW;
   
END;
$$;

--
-- TOC entry 3649 (class 0 OID 88771)
-- Dependencies: 221
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.auth_group VALUES (1, 'Admin');
INSERT INTO public.auth_group VALUES (3, 'Editor');
INSERT INTO public.auth_group VALUES (2, 'Moderator');
INSERT INTO public.auth_group VALUES (4, 'Viewer');


--
-- TOC entry 3651 (class 0 OID 88779)
-- Dependencies: 223
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.auth_group_permissions VALUES (199, 1, 33);
INSERT INTO public.auth_group_permissions VALUES (200, 1, 65);
INSERT INTO public.auth_group_permissions VALUES (201, 1, 4);
INSERT INTO public.auth_group_permissions VALUES (202, 1, 37);
INSERT INTO public.auth_group_permissions VALUES (203, 1, 5);
INSERT INTO public.auth_group_permissions VALUES (204, 1, 73);
INSERT INTO public.auth_group_permissions VALUES (205, 1, 13);
INSERT INTO public.auth_group_permissions VALUES (206, 1, 49);
INSERT INTO public.auth_group_permissions VALUES (207, 1, 81);
INSERT INTO public.auth_group_permissions VALUES (208, 1, 61);
INSERT INTO public.auth_group_permissions VALUES (209, 1, 53);
INSERT INTO public.auth_group_permissions VALUES (210, 1, 85);
INSERT INTO public.auth_group_permissions VALUES (211, 1, 89);
INSERT INTO public.auth_group_permissions VALUES (212, 1, 93);
INSERT INTO public.auth_group_permissions VALUES (213, 1, 25);
INSERT INTO public.auth_group_permissions VALUES (214, 1, 57);
INSERT INTO public.auth_group_permissions VALUES (215, 1, 6);
INSERT INTO public.auth_group_permissions VALUES (216, 1, 8);
INSERT INTO public.auth_group_permissions VALUES (217, 1, 12);
INSERT INTO public.auth_group_permissions VALUES (218, 1, 14);
INSERT INTO public.auth_group_permissions VALUES (219, 1, 16);
INSERT INTO public.auth_group_permissions VALUES (220, 1, 20);
INSERT INTO public.auth_group_permissions VALUES (221, 1, 24);
INSERT INTO public.auth_group_permissions VALUES (222, 1, 26);
INSERT INTO public.auth_group_permissions VALUES (223, 1, 27);
INSERT INTO public.auth_group_permissions VALUES (224, 1, 28);
INSERT INTO public.auth_group_permissions VALUES (225, 1, 34);
INSERT INTO public.auth_group_permissions VALUES (226, 1, 35);
INSERT INTO public.auth_group_permissions VALUES (227, 1, 36);
INSERT INTO public.auth_group_permissions VALUES (228, 1, 38);
INSERT INTO public.auth_group_permissions VALUES (229, 1, 39);
INSERT INTO public.auth_group_permissions VALUES (230, 1, 40);
INSERT INTO public.auth_group_permissions VALUES (231, 1, 50);
INSERT INTO public.auth_group_permissions VALUES (232, 1, 51);
INSERT INTO public.auth_group_permissions VALUES (233, 1, 52);
INSERT INTO public.auth_group_permissions VALUES (234, 1, 54);
INSERT INTO public.auth_group_permissions VALUES (235, 1, 55);
INSERT INTO public.auth_group_permissions VALUES (236, 1, 56);
INSERT INTO public.auth_group_permissions VALUES (237, 1, 58);
INSERT INTO public.auth_group_permissions VALUES (238, 1, 59);
INSERT INTO public.auth_group_permissions VALUES (239, 1, 60);
INSERT INTO public.auth_group_permissions VALUES (240, 1, 62);
INSERT INTO public.auth_group_permissions VALUES (241, 1, 63);
INSERT INTO public.auth_group_permissions VALUES (242, 1, 64);
INSERT INTO public.auth_group_permissions VALUES (243, 1, 66);
INSERT INTO public.auth_group_permissions VALUES (244, 1, 67);
INSERT INTO public.auth_group_permissions VALUES (245, 1, 68);
INSERT INTO public.auth_group_permissions VALUES (246, 1, 74);
INSERT INTO public.auth_group_permissions VALUES (247, 1, 75);
INSERT INTO public.auth_group_permissions VALUES (248, 1, 76);
INSERT INTO public.auth_group_permissions VALUES (249, 1, 82);
INSERT INTO public.auth_group_permissions VALUES (250, 1, 83);
INSERT INTO public.auth_group_permissions VALUES (251, 1, 84);
INSERT INTO public.auth_group_permissions VALUES (252, 1, 86);
INSERT INTO public.auth_group_permissions VALUES (253, 1, 87);
INSERT INTO public.auth_group_permissions VALUES (254, 1, 88);
INSERT INTO public.auth_group_permissions VALUES (255, 1, 90);
INSERT INTO public.auth_group_permissions VALUES (256, 1, 91);
INSERT INTO public.auth_group_permissions VALUES (257, 1, 92);
INSERT INTO public.auth_group_permissions VALUES (258, 1, 94);
INSERT INTO public.auth_group_permissions VALUES (259, 1, 95);
INSERT INTO public.auth_group_permissions VALUES (260, 1, 96);
INSERT INTO public.auth_group_permissions VALUES (261, 3, 25);
INSERT INTO public.auth_group_permissions VALUES (262, 3, 26);
INSERT INTO public.auth_group_permissions VALUES (263, 3, 28);
INSERT INTO public.auth_group_permissions VALUES (264, 3, 33);
INSERT INTO public.auth_group_permissions VALUES (265, 3, 34);
INSERT INTO public.auth_group_permissions VALUES (266, 3, 36);
INSERT INTO public.auth_group_permissions VALUES (267, 3, 37);
INSERT INTO public.auth_group_permissions VALUES (268, 3, 38);
INSERT INTO public.auth_group_permissions VALUES (269, 3, 40);
INSERT INTO public.auth_group_permissions VALUES (270, 3, 49);
INSERT INTO public.auth_group_permissions VALUES (271, 3, 50);
INSERT INTO public.auth_group_permissions VALUES (272, 3, 52);
INSERT INTO public.auth_group_permissions VALUES (273, 3, 53);
INSERT INTO public.auth_group_permissions VALUES (274, 3, 54);
INSERT INTO public.auth_group_permissions VALUES (275, 3, 56);
INSERT INTO public.auth_group_permissions VALUES (276, 3, 57);
INSERT INTO public.auth_group_permissions VALUES (277, 3, 58);
INSERT INTO public.auth_group_permissions VALUES (278, 3, 60);
INSERT INTO public.auth_group_permissions VALUES (279, 3, 61);
INSERT INTO public.auth_group_permissions VALUES (280, 3, 62);
INSERT INTO public.auth_group_permissions VALUES (281, 3, 64);
INSERT INTO public.auth_group_permissions VALUES (282, 3, 65);
INSERT INTO public.auth_group_permissions VALUES (283, 3, 66);
INSERT INTO public.auth_group_permissions VALUES (284, 3, 68);
INSERT INTO public.auth_group_permissions VALUES (285, 3, 73);
INSERT INTO public.auth_group_permissions VALUES (286, 3, 74);
INSERT INTO public.auth_group_permissions VALUES (287, 3, 76);
INSERT INTO public.auth_group_permissions VALUES (288, 3, 81);
INSERT INTO public.auth_group_permissions VALUES (289, 3, 82);
INSERT INTO public.auth_group_permissions VALUES (290, 3, 84);
INSERT INTO public.auth_group_permissions VALUES (291, 3, 85);
INSERT INTO public.auth_group_permissions VALUES (292, 3, 86);
INSERT INTO public.auth_group_permissions VALUES (293, 3, 88);
INSERT INTO public.auth_group_permissions VALUES (294, 3, 89);
INSERT INTO public.auth_group_permissions VALUES (295, 3, 90);
INSERT INTO public.auth_group_permissions VALUES (296, 3, 92);
INSERT INTO public.auth_group_permissions VALUES (297, 3, 93);
INSERT INTO public.auth_group_permissions VALUES (298, 3, 94);
INSERT INTO public.auth_group_permissions VALUES (299, 3, 96);
INSERT INTO public.auth_group_permissions VALUES (300, 2, 25);
INSERT INTO public.auth_group_permissions VALUES (301, 2, 26);
INSERT INTO public.auth_group_permissions VALUES (302, 2, 27);
INSERT INTO public.auth_group_permissions VALUES (303, 2, 28);
INSERT INTO public.auth_group_permissions VALUES (304, 2, 33);
INSERT INTO public.auth_group_permissions VALUES (305, 2, 34);
INSERT INTO public.auth_group_permissions VALUES (306, 2, 35);
INSERT INTO public.auth_group_permissions VALUES (307, 2, 36);
INSERT INTO public.auth_group_permissions VALUES (308, 2, 37);
INSERT INTO public.auth_group_permissions VALUES (309, 2, 38);
INSERT INTO public.auth_group_permissions VALUES (310, 2, 39);
INSERT INTO public.auth_group_permissions VALUES (311, 2, 40);
INSERT INTO public.auth_group_permissions VALUES (312, 2, 49);
INSERT INTO public.auth_group_permissions VALUES (313, 2, 50);
INSERT INTO public.auth_group_permissions VALUES (314, 2, 51);
INSERT INTO public.auth_group_permissions VALUES (315, 2, 52);
INSERT INTO public.auth_group_permissions VALUES (316, 2, 53);
INSERT INTO public.auth_group_permissions VALUES (317, 2, 54);
INSERT INTO public.auth_group_permissions VALUES (318, 2, 55);
INSERT INTO public.auth_group_permissions VALUES (319, 2, 56);
INSERT INTO public.auth_group_permissions VALUES (320, 2, 57);
INSERT INTO public.auth_group_permissions VALUES (321, 2, 58);
INSERT INTO public.auth_group_permissions VALUES (322, 2, 59);
INSERT INTO public.auth_group_permissions VALUES (323, 2, 60);
INSERT INTO public.auth_group_permissions VALUES (324, 2, 61);
INSERT INTO public.auth_group_permissions VALUES (325, 2, 62);
INSERT INTO public.auth_group_permissions VALUES (326, 2, 63);
INSERT INTO public.auth_group_permissions VALUES (327, 2, 64);
INSERT INTO public.auth_group_permissions VALUES (328, 2, 65);
INSERT INTO public.auth_group_permissions VALUES (329, 2, 66);
INSERT INTO public.auth_group_permissions VALUES (330, 2, 67);
INSERT INTO public.auth_group_permissions VALUES (331, 2, 68);
INSERT INTO public.auth_group_permissions VALUES (332, 2, 73);
INSERT INTO public.auth_group_permissions VALUES (333, 2, 74);
INSERT INTO public.auth_group_permissions VALUES (334, 2, 75);
INSERT INTO public.auth_group_permissions VALUES (335, 2, 76);
INSERT INTO public.auth_group_permissions VALUES (336, 2, 81);
INSERT INTO public.auth_group_permissions VALUES (337, 2, 82);
INSERT INTO public.auth_group_permissions VALUES (338, 2, 83);
INSERT INTO public.auth_group_permissions VALUES (339, 2, 84);
INSERT INTO public.auth_group_permissions VALUES (340, 2, 85);
INSERT INTO public.auth_group_permissions VALUES (341, 2, 86);
INSERT INTO public.auth_group_permissions VALUES (342, 2, 87);
INSERT INTO public.auth_group_permissions VALUES (343, 2, 88);
INSERT INTO public.auth_group_permissions VALUES (344, 2, 89);
INSERT INTO public.auth_group_permissions VALUES (345, 2, 90);
INSERT INTO public.auth_group_permissions VALUES (346, 2, 91);
INSERT INTO public.auth_group_permissions VALUES (347, 2, 92);
INSERT INTO public.auth_group_permissions VALUES (348, 2, 93);
INSERT INTO public.auth_group_permissions VALUES (349, 2, 94);
INSERT INTO public.auth_group_permissions VALUES (350, 2, 95);
INSERT INTO public.auth_group_permissions VALUES (351, 2, 96);
INSERT INTO public.auth_group_permissions VALUES (352, 4, 96);
INSERT INTO public.auth_group_permissions VALUES (353, 4, 64);
INSERT INTO public.auth_group_permissions VALUES (354, 4, 36);
INSERT INTO public.auth_group_permissions VALUES (355, 4, 68);
INSERT INTO public.auth_group_permissions VALUES (356, 4, 40);
INSERT INTO public.auth_group_permissions VALUES (357, 4, 76);
INSERT INTO public.auth_group_permissions VALUES (358, 4, 60);
INSERT INTO public.auth_group_permissions VALUES (359, 4, 92);
INSERT INTO public.auth_group_permissions VALUES (360, 4, 52);
INSERT INTO public.auth_group_permissions VALUES (361, 4, 84);
INSERT INTO public.auth_group_permissions VALUES (362, 4, 56);
INSERT INTO public.auth_group_permissions VALUES (363, 4, 88);
INSERT INTO public.auth_group_permissions VALUES (364, 4, 28);


--
-- TOC entry 3647 (class 0 OID 88765)
-- Dependencies: 219
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.auth_permission VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO public.auth_permission VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO public.auth_permission VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO public.auth_permission VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO public.auth_permission VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO public.auth_permission VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO public.auth_permission VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO public.auth_permission VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO public.auth_permission VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO public.auth_permission VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO public.auth_permission VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO public.auth_permission VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO public.auth_permission VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO public.auth_permission VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO public.auth_permission VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO public.auth_permission VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO public.auth_permission VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO public.auth_permission VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO public.auth_permission VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO public.auth_permission VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO public.auth_permission VALUES (25, 'Can add Album', 7, 'add_album');
INSERT INTO public.auth_permission VALUES (26, 'Can change Album', 7, 'change_album');
INSERT INTO public.auth_permission VALUES (27, 'Can delete Album', 7, 'delete_album');
INSERT INTO public.auth_permission VALUES (28, 'Can view Album', 7, 'view_album');
INSERT INTO public.auth_permission VALUES (33, 'Can add Album Track', 9, 'add_albumtrack');
INSERT INTO public.auth_permission VALUES (34, 'Can change Album Track', 9, 'change_albumtrack');
INSERT INTO public.auth_permission VALUES (35, 'Can delete Album Track', 9, 'delete_albumtrack');
INSERT INTO public.auth_permission VALUES (36, 'Can view Album Track', 9, 'view_albumtrack');
INSERT INTO public.auth_permission VALUES (37, 'Can add Artist', 10, 'add_artist');
INSERT INTO public.auth_permission VALUES (38, 'Can change Artist', 10, 'change_artist');
INSERT INTO public.auth_permission VALUES (39, 'Can delete Artist', 10, 'delete_artist');
INSERT INTO public.auth_permission VALUES (40, 'Can view Artist', 10, 'view_artist');
INSERT INTO public.auth_permission VALUES (49, 'Can add Genre', 13, 'add_genre');
INSERT INTO public.auth_permission VALUES (50, 'Can change Genre', 13, 'change_genre');
INSERT INTO public.auth_permission VALUES (51, 'Can delete Genre', 13, 'delete_genre');
INSERT INTO public.auth_permission VALUES (52, 'Can view Genre', 13, 'view_genre');
INSERT INTO public.auth_permission VALUES (53, 'Can add Playlist', 14, 'add_playlist');
INSERT INTO public.auth_permission VALUES (54, 'Can change Playlist', 14, 'change_playlist');
INSERT INTO public.auth_permission VALUES (55, 'Can delete Playlist', 14, 'delete_playlist');
INSERT INTO public.auth_permission VALUES (56, 'Can view Playlist', 14, 'view_playlist');
INSERT INTO public.auth_permission VALUES (57, 'Can add Song-Playlist Relation', 15, 'add_songplaylistrelation');
INSERT INTO public.auth_permission VALUES (58, 'Can change Song-Playlist Relation', 15, 'change_songplaylistrelation');
INSERT INTO public.auth_permission VALUES (59, 'Can delete Song-Playlist Relation', 15, 'delete_songplaylistrelation');
INSERT INTO public.auth_permission VALUES (60, 'Can view Song-Playlist Relation', 15, 'view_songplaylistrelation');
INSERT INTO public.auth_permission VALUES (61, 'Can add Song', 16, 'add_song');
INSERT INTO public.auth_permission VALUES (62, 'Can change Song', 16, 'change_song');
INSERT INTO public.auth_permission VALUES (63, 'Can delete Song', 16, 'delete_song');
INSERT INTO public.auth_permission VALUES (64, 'Can view Song', 16, 'view_song');
INSERT INTO public.auth_permission VALUES (65, 'Can add Pending Song', 17, 'add_pendingsong');
INSERT INTO public.auth_permission VALUES (66, 'Can change Pending Song', 17, 'change_pendingsong');
INSERT INTO public.auth_permission VALUES (67, 'Can delete Pending Song', 17, 'delete_pendingsong');
INSERT INTO public.auth_permission VALUES (68, 'Can view Pending Song', 17, 'view_pendingsong');
INSERT INTO public.auth_permission VALUES (73, 'Can add Music Group', 12, 'add_musicgroup');
INSERT INTO public.auth_permission VALUES (74, 'Can change Music Group', 12, 'change_musicgroup');
INSERT INTO public.auth_permission VALUES (75, 'Can delete Music Group', 12, 'delete_musicgroup');
INSERT INTO public.auth_permission VALUES (76, 'Can view Music Group', 12, 'view_musicgroup');
INSERT INTO public.auth_permission VALUES (81, 'Can add Task Comment', 19, 'add_taskcomment');
INSERT INTO public.auth_permission VALUES (82, 'Can change Task Comment', 19, 'change_taskcomment');
INSERT INTO public.auth_permission VALUES (83, 'Can delete Task Comment', 19, 'delete_taskcomment');
INSERT INTO public.auth_permission VALUES (84, 'Can view Task Comment', 19, 'view_taskcomment');
INSERT INTO public.auth_permission VALUES (85, 'Can add Task', 20, 'add_task');
INSERT INTO public.auth_permission VALUES (86, 'Can change Task', 20, 'change_task');
INSERT INTO public.auth_permission VALUES (87, 'Can delete Task', 20, 'delete_task');
INSERT INTO public.auth_permission VALUES (88, 'Can view Task', 20, 'view_task');
INSERT INTO public.auth_permission VALUES (89, 'Can add Album Link', 8, 'add_albumlink');
INSERT INTO public.auth_permission VALUES (90, 'Can change Album Link', 8, 'change_albumlink');
INSERT INTO public.auth_permission VALUES (91, 'Can delete Album Link', 8, 'delete_albumlink');
INSERT INTO public.auth_permission VALUES (92, 'Can view Album Link', 8, 'view_albumlink');
INSERT INTO public.auth_permission VALUES (93, 'Can add Artist Link', 11, 'add_artistlink');
INSERT INTO public.auth_permission VALUES (94, 'Can change Artist Link', 11, 'change_artistlink');
INSERT INTO public.auth_permission VALUES (95, 'Can delete Artist Link', 11, 'delete_artistlink');
INSERT INTO public.auth_permission VALUES (96, 'Can view Artist Link', 11, 'view_artistlink');


--
-- TOC entry 3645 (class 0 OID 88757)
-- Dependencies: 217
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.django_content_type VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type VALUES (2, 'auth', 'permission');
INSERT INTO public.django_content_type VALUES (3, 'auth', 'group');
INSERT INTO public.django_content_type VALUES (4, 'auth', 'user');
INSERT INTO public.django_content_type VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type VALUES (6, 'sessions', 'session');
INSERT INTO public.django_content_type VALUES (7, 'albums', 'album');
INSERT INTO public.django_content_type VALUES (9, 'albums', 'albumtrack');
INSERT INTO public.django_content_type VALUES (10, 'artists', 'artist');
INSERT INTO public.django_content_type VALUES (13, 'common', 'genre');
INSERT INTO public.django_content_type VALUES (14, 'playlists', 'playlist');
INSERT INTO public.django_content_type VALUES (15, 'playlists', 'songplaylistrelation');
INSERT INTO public.django_content_type VALUES (16, 'songs', 'song');
INSERT INTO public.django_content_type VALUES (17, 'songs', 'pendingsong');
INSERT INTO public.django_content_type VALUES (12, 'common', 'musicgroup');
INSERT INTO public.django_content_type VALUES (19, 'tasks', 'taskcomment');
INSERT INTO public.django_content_type VALUES (20, 'tasks', 'task');
INSERT INTO public.django_content_type VALUES (8, 'albums', 'albumlink');
INSERT INTO public.django_content_type VALUES (11, 'artists', 'artistlink');


--
-- TOC entry 3493 (class 2620 OID 89340)
-- Name: songs tr_update_after_change_of_spotify_link_on_song; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_after_change_of_spotify_link_on_song AFTER UPDATE ON public.songs FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_calc_songs_spotify();


--
-- TOC entry 3491 (class 2620 OID 89164)
-- Name: albums tr_update_after_change_on_albums; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_after_change_on_albums AFTER INSERT OR DELETE ON public.albums FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_calc_albums_count();


--
-- TOC entry 3495 (class 2620 OID 89166)
-- Name: pending_songs tr_update_after_change_on_pending_songs; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_after_change_on_pending_songs AFTER INSERT OR DELETE ON public.pending_songs FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_calc_pending_count();


--
-- TOC entry 3497 (class 2620 OID 89337)
-- Name: song_playlist_relations tr_update_after_change_on_song_playlist_relations; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_after_change_on_song_playlist_relations AFTER INSERT OR DELETE ON public.song_playlist_relations FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_calc_on_playlist_songs_count();


--
-- TOC entry 3494 (class 2620 OID 89172)
-- Name: songs tr_update_after_change_on_songs; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_after_change_on_songs AFTER INSERT OR DELETE ON public.songs FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_calc_check_all_variables_from_songs();


--
-- TOC entry 3492 (class 2620 OID 89160)
-- Name: albums tr_update_after_insert_on_albums; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_after_insert_on_albums AFTER INSERT ON public.albums FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_insert_new_album_to_albums_sites();


--
-- TOC entry 3489 (class 2620 OID 89162)
-- Name: artists tr_update_after_insert_on_artists; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_after_insert_on_artists AFTER INSERT ON public.artists FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_insert_new_artist_to_artists_sites();


--
-- TOC entry 3490 (class 2620 OID 89168)
-- Name: artists tr_update_pending_after_change_on_artists; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_pending_after_change_on_artists AFTER INSERT OR DELETE ON public.artists FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_check_if_artist_exist();


--
-- TOC entry 3496 (class 2620 OID 89170)
-- Name: pending_songs tr_update_pending_after_new_add; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tr_update_pending_after_new_add AFTER INSERT ON public.pending_songs FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_check_new_add_on_pending();


