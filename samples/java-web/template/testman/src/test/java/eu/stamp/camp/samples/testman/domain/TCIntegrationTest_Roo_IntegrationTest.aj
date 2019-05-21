// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package eu.stamp.camp.samples.testman.domain;

import eu.stamp.camp.samples.testman.domain.TC;
import eu.stamp.camp.samples.testman.domain.TCDataOnDemand;
import eu.stamp.camp.samples.testman.domain.TCIntegrationTest;
import java.util.Iterator;
import java.util.List;
import javax.validation.ConstraintViolation;
import javax.validation.ConstraintViolationException;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.transaction.annotation.Transactional;

privileged aspect TCIntegrationTest_Roo_IntegrationTest {
    
    declare @type: TCIntegrationTest: @RunWith(SpringJUnit4ClassRunner.class);
    
    declare @type: TCIntegrationTest: @ContextConfiguration(locations = "classpath*:/META-INF/spring/applicationContext*.xml");
    
    declare @type: TCIntegrationTest: @Transactional;
    
    @Autowired
    TCDataOnDemand TCIntegrationTest.dod;
    
    @Test
    public void TCIntegrationTest.testCountTCS() {
        Assert.assertNotNull("Data on demand for 'TC' failed to initialize correctly", dod.getRandomTC());
        long count = TC.countTCS();
        Assert.assertTrue("Counter for 'TC' incorrectly reported there were no entries", count > 0);
    }
    
    @Test
    public void TCIntegrationTest.testFindTC() {
        TC obj = dod.getRandomTC();
        Assert.assertNotNull("Data on demand for 'TC' failed to initialize correctly", obj);
        Long id = obj.getId();
        Assert.assertNotNull("Data on demand for 'TC' failed to provide an identifier", id);
        obj = TC.findTC(id);
        Assert.assertNotNull("Find method for 'TC' illegally returned null for id '" + id + "'", obj);
        Assert.assertEquals("Find method for 'TC' returned the incorrect identifier", id, obj.getId());
    }
    
    @Test
    public void TCIntegrationTest.testFindAllTCS() {
        Assert.assertNotNull("Data on demand for 'TC' failed to initialize correctly", dod.getRandomTC());
        long count = TC.countTCS();
        Assert.assertTrue("Too expensive to perform a find all test for 'TC', as there are " + count + " entries; set the findAllMaximum to exceed this value or set findAll=false on the integration test annotation to disable the test", count < 250);
        List<TC> result = TC.findAllTCS();
        Assert.assertNotNull("Find all method for 'TC' illegally returned null", result);
        Assert.assertTrue("Find all method for 'TC' failed to return any data", result.size() > 0);
    }
    
    @Test
    public void TCIntegrationTest.testFindTCEntries() {
        Assert.assertNotNull("Data on demand for 'TC' failed to initialize correctly", dod.getRandomTC());
        long count = TC.countTCS();
        if (count > 20) count = 20;
        int firstResult = 0;
        int maxResults = (int) count;
        List<TC> result = TC.findTCEntries(firstResult, maxResults);
        Assert.assertNotNull("Find entries method for 'TC' illegally returned null", result);
        Assert.assertEquals("Find entries method for 'TC' returned an incorrect number of entries", count, result.size());
    }
    
    @Test
    public void TCIntegrationTest.testFlush() {
        TC obj = dod.getRandomTC();
        Assert.assertNotNull("Data on demand for 'TC' failed to initialize correctly", obj);
        Long id = obj.getId();
        Assert.assertNotNull("Data on demand for 'TC' failed to provide an identifier", id);
        obj = TC.findTC(id);
        Assert.assertNotNull("Find method for 'TC' illegally returned null for id '" + id + "'", obj);
        boolean modified =  dod.modifyTC(obj);
        Integer currentVersion = obj.getVersion();
        obj.flush();
        Assert.assertTrue("Version for 'TC' failed to increment on flush directive", (currentVersion != null && obj.getVersion() > currentVersion) || !modified);
    }
    
    @Test
    public void TCIntegrationTest.testMergeUpdate() {
        TC obj = dod.getRandomTC();
        Assert.assertNotNull("Data on demand for 'TC' failed to initialize correctly", obj);
        Long id = obj.getId();
        Assert.assertNotNull("Data on demand for 'TC' failed to provide an identifier", id);
        obj = TC.findTC(id);
        boolean modified =  dod.modifyTC(obj);
        Integer currentVersion = obj.getVersion();
        TC merged = obj.merge();
        obj.flush();
        Assert.assertEquals("Identifier of merged object not the same as identifier of original object", merged.getId(), id);
        Assert.assertTrue("Version for 'TC' failed to increment on merge and flush directive", (currentVersion != null && obj.getVersion() > currentVersion) || !modified);
    }
    
    @Test
    public void TCIntegrationTest.testPersist() {
        Assert.assertNotNull("Data on demand for 'TC' failed to initialize correctly", dod.getRandomTC());
        TC obj = dod.getNewTransientTC(Integer.MAX_VALUE);
        Assert.assertNotNull("Data on demand for 'TC' failed to provide a new transient entity", obj);
        Assert.assertNull("Expected 'TC' identifier to be null", obj.getId());
        try {
            obj.persist();
        } catch (final ConstraintViolationException e) {
            final StringBuilder msg = new StringBuilder();
            for (Iterator<ConstraintViolation<?>> iter = e.getConstraintViolations().iterator(); iter.hasNext();) {
                final ConstraintViolation<?> cv = iter.next();
                msg.append("[").append(cv.getRootBean().getClass().getName()).append(".").append(cv.getPropertyPath()).append(": ").append(cv.getMessage()).append(" (invalid value = ").append(cv.getInvalidValue()).append(")").append("]");
            }
            throw new IllegalStateException(msg.toString(), e);
        }
        obj.flush();
        Assert.assertNotNull("Expected 'TC' identifier to no longer be null", obj.getId());
    }
    
    @Test
    public void TCIntegrationTest.testRemove() {
        TC obj = dod.getRandomTC();
        Assert.assertNotNull("Data on demand for 'TC' failed to initialize correctly", obj);
        Long id = obj.getId();
        Assert.assertNotNull("Data on demand for 'TC' failed to provide an identifier", id);
        obj = TC.findTC(id);
        obj.remove();
        obj.flush();
        Assert.assertNull("Failed to remove 'TC' with identifier '" + id + "'", TC.findTC(id));
    }
    
}
