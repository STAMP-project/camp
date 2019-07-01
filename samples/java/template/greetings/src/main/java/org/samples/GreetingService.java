/*
 * CAMP
 *
 * Copyright (C) 2017, 2018 SINTEF Digital
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the MIT license.  See the LICENSE file for details.
 */

package org.samples;


import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.core.Response;


@Path("/hello")
public class GreetingService {

	// static {
	// 	System.setProperty("http.proxyHost", "proxy.eng.it");
	// 	System.setProperty("http.proxyPort", "3128");
	// 	System.setProperty("https.proxyHost", "proxy.eng.it");
	// 	System.setProperty("https.proxyPort", "3128");
	// }

	@GET
	@Path("/{name}")
	public Response getMessage(@PathParam("name") String name) {

	    final String output = String.format("Hello '%s'!", name);

	    return Response.status(200).entity(output).build();
	}

}
