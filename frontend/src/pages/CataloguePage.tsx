import React, { useEffect, useState, useMemo, useCallback } from 'react';
import {
  Search,
  Filter,
  BookOpen,
  ExternalLink,
  Shield,
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  X,
  RotateCcw,
  Info,
  Calendar,
  Layers,
  Sparkles,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  HelpCircle,
  FileText
} from 'lucide-react';
import { http, errMsg } from '../api';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Alert } from '../components/ui/Alert';
import { MedicalDisclaimer } from '../components/MedicalDisclaimer';

interface CatalogueItem {
  supplement_id: string;
  supplement_name: string;
  supplement_category: string;
  verification_status: string;
  source_url?: string;
  description?: string;
  active_ingredients?: string;
  ingredient_forms?: string;
}

interface GoalMapping {
  mapping_id: string;
  supplement_id: string;
  goal_id: string;
  match_type: string;
  match_score: string | number;
  evidence_notes?: string;
}

interface SafetyRule {
  rule_id: string;
  supplement_id: string;
  rule_type: string;
  condition_code: string;
  action: 'exclude' | 'review' | string;
  safety_message: string;
}

interface DietCompat {
  supplement_id: string;
  diet_code: string;
  compat_status: string;
  source_ref?: string;
  notes?: string;
}

interface AllergenRecord {
  supplement_id: string;
  allergen_code: string;
  relation?: string;
  source_ref?: string;
  notes?: string;
}

interface SupplementDetail extends CatalogueItem {
  primary_source_id?: string;
  last_reviewed_at?: string;
  is_active?: string;
  notes?: string;
  goal_mappings?: GoalMapping[];
  diet_compat?: DietCompat[];
  safety_rules?: SafetyRule[];
  allergens?: AllergenRecord[];
  note?: string;
}

const CATEGORY_LABELS: Record<string, string> = {
  vitamin: 'Vitamin & Complexes',
  mineral: 'Mineral & Trace Elements',
  nutrient: 'Nutrient & Antioxidant',
  fatty_acid: 'Omega-3 & Fatty Acids',
  protein_amino_acid: 'Protein Supplements',
  amino_acid_derivative: 'Amino Acids & Derivatives',
  electrolyte: 'Electrolytes & Hydration',
  fiber_prebiotic: 'Fiber & Prebiotics',
  probiotic: 'Probiotics & Microbes',
  botanical: 'Herbal & Botanical',
  hormone_supplement: 'Hormone Supplement',
};

const formatCategory = (cat: string): string => {
  if (!cat) return '';
  return CATEGORY_LABELS[cat] || cat.split('_').map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
};

export const CataloguePage: React.FC = () => {
  const [items, setItems] = useState<CatalogueItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [sortBy, setSortBy] = useState('name_asc');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(24);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState<SupplementDetail | null>(null);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [showMobileFilters, setShowMobileFilters] = useState(false);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(searchQuery.trim());
      setCurrentPage(1);
    }, 250);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  const fetchCatalogue = useCallback(async () => {
    setIsLoading(true);
    setErrorMsg('');
    try {
      const res = await http.get('/catalogue', {
        params: {
          q: debouncedQuery,
          category: selectedCategory,
          status: selectedStatus,
          sort: sortBy,
        },
      });
      setItems(res.data || []);
      setCurrentPage(1);
    } catch (err: any) {
      setErrorMsg(errMsg(err));
    } finally {
      setIsLoading(false);
    }
  }, [debouncedQuery, selectedCategory, selectedStatus, sortBy]);

  useEffect(() => {
    fetchCatalogue();
  }, [fetchCatalogue]);

  // Handle escape key to close details modal
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && selectedItem) {
        setSelectedItem(null);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedItem]);

  const openDetails = async (sid: string) => {
    setIsDetailLoading(true);
    try {
      const res = await http.get(`/catalogue/${sid}`);
      setSelectedItem(res.data);
    } catch (err: any) {
      setErrorMsg(errMsg(err));
    } finally {
      setIsDetailLoading(false);
    }
  };

  const handleResetFilters = () => {
    setSearchQuery('');
    setDebouncedQuery('');
    setSelectedCategory('');
    setSelectedStatus('');
    setSortBy('name_asc');
    setCurrentPage(1);
  };

  const hasActiveFilters = Boolean(searchQuery.trim() || selectedCategory || selectedStatus || sortBy !== 'name_asc');

  // Pagination calculations
  const totalPages = itemsPerPage > 0 ? Math.max(1, Math.ceil(items.length / itemsPerPage)) : 1;
  const paginatedItems = useMemo(() => {
    if (itemsPerPage === 0) return items;
    const start = (currentPage - 1) * itemsPerPage;
    return items.slice(start, start + itemsPerPage);
  }, [items, currentPage, itemsPerPage]);

  // Discover distinct categories present in dataset
  const availableCategories = useMemo(() => {
    const set = new Set<string>();
    items.forEach((item) => {
      if (item.supplement_category) set.add(item.supplement_category);
    });
    // Fallback to standard categories if empty or filtered
    Object.keys(CATEGORY_LABELS).forEach((cat) => set.add(cat));
    return Array.from(set).sort();
  }, [items]);

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-[#E5E5DD]">
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-[#244B38] mb-1">
            <BookOpen className="h-3.5 w-3.5" aria-hidden="true" />
            <span>Monograph Database</span>
          </div>
          <h1 className="text-2xl font-bold text-[#252923] tracking-tight">
            Supplement Catalogue
          </h1>
          <p className="mt-1 text-xs sm:text-sm text-[#73796F] max-w-2xl leading-relaxed">
            Explore verified supplement reference data, active ingredients, commercial forms, dietary compatibility, and interaction rules from authoritative monographs.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Badge variant="neutral" size="md">
            <span>{items.length} {items.length === 1 ? 'record' : 'records'} available</span>
          </Badge>
        </div>
      </div>

      {/* Error state */}
      {errorMsg && (
        <Alert variant="danger" title="Unable to retrieve supplement catalogue">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mt-1">
            <span>{errorMsg}</span>
            <Button
              variant="outline"
              size="sm"
              onClick={fetchCatalogue}
              className="shrink-0 text-xs"
            >
              <RotateCcw className="h-3.5 w-3.5 mr-1" />
              <span>Retry</span>
            </Button>
          </div>
        </Alert>
      )}

      {/* Search & Filter Toolbar */}
      <Card bordered className="bg-white">
        <CardContent className="p-4 sm:p-5 space-y-3">
          <div className="flex flex-col lg:flex-row items-stretch lg:items-center gap-3">
            {/* Search Input */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#73796F]" aria-hidden="true" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by supplement name, description, or active ingredient..."
                aria-label="Search supplement catalogue"
                className="w-full rounded-lg border border-[#E5E5DD] bg-white py-2 pl-9 pr-9 text-xs text-[#252923] placeholder:text-[#8E9589] focus:border-[#244B38] focus:outline-none focus:ring-1 focus:ring-[#244B38] transition-colors"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  aria-label="Clear search query"
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 p-1 text-[#73796F] hover:text-[#252923] rounded transition-colors"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
              )}
            </div>

            {/* Mobile Filter Toggle */}
            <div className="flex lg:hidden items-center justify-between gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowMobileFilters(!showMobileFilters)}
                className="text-xs w-full justify-between"
              >
                <span className="flex items-center gap-1.5">
                  <Filter className="h-3.5 w-3.5 text-[#5E645A]" />
                  <span>Filters &amp; Sorting</span>
                </span>
                <ChevronDown className={`h-3.5 w-3.5 transition-transform ${showMobileFilters ? 'rotate-180' : ''}`} />
              </Button>
              {hasActiveFilters && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleResetFilters}
                  className="text-xs text-[#73796F] hover:text-[#244B38] shrink-0"
                >
                  Reset
                </Button>
              )}
            </div>

            {/* Desktop Filters & Sort Controls */}
            <div className={`grid grid-cols-1 sm:grid-cols-3 lg:flex items-center gap-2.5 ${showMobileFilters ? 'grid' : 'hidden lg:flex'}`}>
              {/* Category Filter */}
              <div className="min-w-[150px]">
                <label htmlFor="filter-category" className="sr-only">Category</label>
                <select
                  id="filter-category"
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full rounded-lg border border-[#E5E5DD] bg-white py-2 px-2.5 text-xs text-[#252923] focus:border-[#244B38] focus:outline-none focus:ring-1 focus:ring-[#244B38] transition-colors cursor-pointer"
                >
                  <option value="">All Categories</option>
                  {availableCategories.map((c) => (
                    <option key={c} value={c}>
                      {formatCategory(c)}
                    </option>
                  ))}
                </select>
              </div>

              {/* Status Filter */}
              <div className="min-w-[140px]">
                <label htmlFor="filter-status" className="sr-only">Verification Status</label>
                <select
                  id="filter-status"
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value)}
                  className="w-full rounded-lg border border-[#E5E5DD] bg-white py-2 px-2.5 text-xs text-[#252923] focus:border-[#244B38] focus:outline-none focus:ring-1 focus:ring-[#244B38] transition-colors cursor-pointer"
                >
                  <option value="">All Statuses</option>
                  <option value="verified">Verified Only</option>
                  <option value="needs_review">Needs Review</option>
                </select>
              </div>

              {/* Sort By */}
              <div className="min-w-[150px]">
                <label htmlFor="filter-sort" className="sr-only">Sort Order</label>
                <select
                  id="filter-sort"
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full rounded-lg border border-[#E5E5DD] bg-white py-2 px-2.5 text-xs text-[#252923] focus:border-[#244B38] focus:outline-none focus:ring-1 focus:ring-[#244B38] transition-colors cursor-pointer"
                >
                  <option value="name_asc">Name (A to Z)</option>
                  <option value="name_desc">Name (Z to A)</option>
                  <option value="category">Category</option>
                </select>
              </div>

              {/* Reset Action (Desktop) */}
              {hasActiveFilters && (
                <button
                  type="button"
                  onClick={handleResetFilters}
                  title="Reset all filters and search"
                  className="hidden lg:inline-flex items-center gap-1 px-2.5 py-2 text-xs font-medium text-[#73796F] hover:text-[#244B38] rounded-lg border border-transparent hover:border-[#E5E5DD] transition-colors cursor-pointer"
                >
                  <RotateCcw className="h-3 w-3" />
                  <span>Reset</span>
                </button>
              )}
            </div>
          </div>

          {/* Active Filter Indicators */}
          {hasActiveFilters && (
            <div className="pt-2 border-t border-[#F2F2EC] flex flex-wrap items-center gap-1.5 text-xs">
              <span className="text-[11px] font-medium text-[#73796F]">Active filters:</span>
              {searchQuery.trim() && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#F4F4EE] text-[#252923] text-[11px] border border-[#E5E5DD]">
                  <span>Query: &ldquo;{searchQuery.trim()}&rdquo;</span>
                  <button
                    type="button"
                    onClick={() => setSearchQuery('')}
                    className="hover:text-[#9E2A2B]"
                    aria-label="Remove search query filter"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
              {selectedCategory && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#F4F4EE] text-[#252923] text-[11px] border border-[#E5E5DD]">
                  <span>Category: {formatCategory(selectedCategory)}</span>
                  <button
                    type="button"
                    onClick={() => setSelectedCategory('')}
                    className="hover:text-[#9E2A2B]"
                    aria-label="Remove category filter"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
              {selectedStatus && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#F4F4EE] text-[#252923] text-[11px] border border-[#E5E5DD]">
                  <span>Status: {selectedStatus === 'verified' ? 'Verified' : 'Needs Review'}</span>
                  <button
                    type="button"
                    onClick={() => setSelectedStatus('')}
                    className="hover:text-[#9E2A2B]"
                    aria-label="Remove status filter"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
              {sortBy !== 'name_asc' && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#F4F4EE] text-[#252923] text-[11px] border border-[#E5E5DD]">
                  <span>Sort: {sortBy === 'name_desc' ? 'Z to A' : 'Category'}</span>
                  <button
                    type="button"
                    onClick={() => setSortBy('name_asc')}
                    className="hover:text-[#9E2A2B]"
                    aria-label="Reset sort order"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
              <button
                type="button"
                onClick={handleResetFilters}
                className="text-[11px] font-semibold text-[#244B38] hover:underline ml-1 cursor-pointer"
              >
                Clear all
              </button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Catalogue Content Area */}
      {isLoading ? (
        <Card bordered className="bg-white">
          <CardContent className="p-12 flex flex-col items-center justify-center text-center space-y-3">
            <LoadingSpinner size="lg" />
            <p className="text-xs font-medium text-[#73796F]">
              Querying supplement monograph records...
            </p>
          </CardContent>
        </Card>
      ) : items.length === 0 ? (
        /* Empty State */
        <Card bordered className="bg-white">
          <CardContent className="p-10 sm:p-14 text-center space-y-3">
            <div className="mx-auto w-10 h-10 rounded-full bg-[#F4F4EE] flex items-center justify-center text-[#73796F]">
              <Search className="h-5 w-5" />
            </div>
            <h3 className="text-sm font-bold text-[#252923]">
              No matching monographs found
            </h3>
            <p className="text-xs text-[#73796F] max-w-md mx-auto leading-relaxed">
              {searchQuery.trim()
                ? `No reference records matched "${searchQuery.trim()}". Check spelling or clear your category and status filters.`
                : 'No supplement records match the current filter selection.'}
            </p>
            {hasActiveFilters && (
              <div className="pt-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleResetFilters}
                  className="text-xs"
                >
                  <RotateCcw className="h-3.5 w-3.5 mr-1.5" />
                  <span>Reset All Filters</span>
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      ) : (
        /* Cards Grid */
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {paginatedItems.map((item) => {
              const isVerified = item.verification_status === 'verified';
              return (
                <Card
                  key={item.supplement_id}
                  bordered
                  className="bg-white flex flex-col justify-between hover:border-[#D5D8CF] transition-colors"
                >
                  <div className="p-5 space-y-3.5">
                    {/* Monograph Top Meta */}
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <span className="font-mono text-[11px] text-[#73796F] tracking-wide block">
                          {item.supplement_id}
                        </span>
                        <h3 className="text-base font-bold text-[#252923] tracking-tight mt-0.5 leading-snug">
                          {item.supplement_name}
                        </h3>
                      </div>
                      <Badge
                        variant={isVerified ? 'safe' : 'review'}
                        size="sm"
                      >
                        {isVerified ? 'Verified' : 'Needs Review'}
                      </Badge>
                    </div>

                    {/* Taxonomy Tags */}
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-[#F4F4EE] text-[#4A5043] border border-[#E5E5DD]">
                        {formatCategory(item.supplement_category)}
                      </span>
                      {item.ingredient_forms && (
                        <span className="text-[11px] text-[#73796F] truncate max-w-[200px]" title={item.ingredient_forms}>
                          Forms: {item.ingredient_forms.split(',')[0]}
                        </span>
                      )}
                    </div>

                    {/* Description */}
                    {item.description && (
                      <p className="text-xs text-[#5E645A] leading-relaxed line-clamp-3">
                        {item.description}
                      </p>
                    )}

                    {/* Active Ingredients Preview */}
                    {item.active_ingredients && (
                      <div className="pt-2 border-t border-[#F5F5F0] text-[11px]">
                        <span className="font-semibold text-[#252923]">Active Composition: </span>
                        <span className="text-[#5E645A] line-clamp-1">{item.active_ingredients}</span>
                      </div>
                    )}
                  </div>

                  {/* Footer Actions */}
                  <div className="px-5 py-3 bg-[#FAF9F5] border-t border-[#E5E5DD] rounded-b-xl flex items-center justify-between">
                    <button
                      type="button"
                      onClick={() => openDetails(item.supplement_id)}
                      className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#244B38] hover:text-[#183627] hover:underline cursor-pointer"
                    >
                      <FileText className="h-3.5 w-3.5" />
                      <span>Inspect Monograph</span>
                    </button>

                    {item.source_url && (
                      <a
                        href={item.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        title="Open authoritative NIH ODS monograph in a new tab"
                        className="text-[#73796F] hover:text-[#244B38] transition-colors p-1 rounded"
                      >
                        <ExternalLink className="h-3.5 w-3.5" />
                        <span className="sr-only">NIH ODS source link</span>
                      </a>
                    )}
                  </div>
                </Card>
              );
            })}
          </div>

          {/* Pagination Toolbar */}
          {totalPages > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-[#E5E5DD]">
              <div className="text-xs text-[#73796F]">
                Showing <span className="font-semibold text-[#252923]">{(currentPage - 1) * (itemsPerPage || items.length) + 1}</span> to{' '}
                <span className="font-semibold text-[#252923]">{itemsPerPage === 0 ? items.length : Math.min(currentPage * itemsPerPage, items.length)}</span> of{' '}
                <span className="font-semibold text-[#252923]">{items.length}</span> supplements
              </div>

              <div className="flex items-center gap-1.5">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="h-8 px-2 text-xs"
                  aria-label="Previous page"
                >
                  <ChevronLeft className="h-3.5 w-3.5 mr-1" />
                  <span>Prev</span>
                </Button>

                <div className="flex items-center gap-1">
                  {Array.from({ length: totalPages }, (_, idx) => idx + 1)
                    .filter((page) => {
                      return (
                        page === 1 ||
                        page === totalPages ||
                        Math.abs(page - currentPage) <= 1
                      );
                    })
                    .reduce<(number | string)[]>((acc, page, idx, arr) => {
                      if (idx > 0 && page - (arr[idx - 1] as number) > 1) {
                        acc.push('...');
                      }
                      acc.push(page);
                      return acc;
                    }, [])
                    .map((p, idx) =>
                      typeof p === 'string' ? (
                        <span key={`ellipsis-${idx}`} className="px-2 text-xs text-[#73796F]">
                          ...
                        </span>
                      ) : (
                        <button
                          key={p}
                          type="button"
                          onClick={() => setCurrentPage(p)}
                          className={`h-8 min-w-[32px] px-2 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
                            currentPage === p
                              ? 'bg-[#244B38] text-white shadow-xs'
                              : 'bg-[#F4F4EE] text-[#4A5043] hover:bg-[#EAEAE2]'
                          }`}
                        >
                          {p}
                        </button>
                      )
                    )}
                </div>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className="h-8 px-2 text-xs"
                  aria-label="Next page"
                >
                  <span>Next</span>
                  <ChevronRight className="h-3.5 w-3.5 ml-1" />
                </Button>
              </div>

              <div className="flex items-center gap-2 text-xs text-[#73796F]">
                <span>Per page:</span>
                <select
                  value={itemsPerPage}
                  onChange={(e) => {
                    setItemsPerPage(Number(e.target.value));
                    setCurrentPage(1);
                  }}
                  className="h-8 px-2 rounded-lg border border-[#D5D8CF] bg-white text-xs text-[#252923] focus:outline-none focus:ring-1 focus:ring-[#244B38]"
                >
                  <option value={12}>12</option>
                  <option value={24}>24</option>
                  <option value={48}>48</option>
                  <option value={0}>All ({items.length})</option>
                </select>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Monograph Detail Modal */}
      {selectedItem && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-monograph-title"
          className="fixed inset-0 z-50 flex items-center justify-center bg-[#252923]/60 p-4 backdrop-blur-xs overflow-y-auto"
        >
          <div className="w-full max-w-2xl rounded-xl bg-white border border-[#E5E5DD] shadow-xl max-h-[90vh] overflow-y-auto space-y-5 p-6 sm:p-7">
            {/* Header */}
            <div className="flex items-start justify-between gap-4 pb-4 border-b border-[#E5E5DD]">
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <h2 id="modal-monograph-title" className="text-xl font-bold text-[#252923] tracking-tight">
                    {selectedItem.supplement_name}
                  </h2>
                  <span className="font-mono text-xs text-[#73796F] bg-[#F4F4EE] px-2 py-0.5 rounded border border-[#E5E5DD]">
                    {selectedItem.supplement_id}
                  </span>
                </div>
                <div className="flex flex-wrap items-center gap-2 mt-2">
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-[#F4F4EE] text-[#4A5043] border border-[#E5E5DD]">
                    {formatCategory(selectedItem.supplement_category)}
                  </span>
                  <Badge
                    variant={selectedItem.verification_status === 'verified' ? 'safe' : 'review'}
                    size="sm"
                  >
                    Verification Status: {selectedItem.verification_status === 'verified' ? 'Verified' : 'Under Review'}
                  </Badge>
                  {selectedItem.last_reviewed_at && (
                    <span className="inline-flex items-center gap-1 text-[11px] text-[#73796F]">
                      <Calendar className="h-3 w-3" />
                      <span>Reviewed: {selectedItem.last_reviewed_at}</span>
                    </span>
                  )}
                </div>
              </div>

              <button
                type="button"
                onClick={() => setSelectedItem(null)}
                aria-label="Close monograph details"
                className="rounded-lg p-1.5 text-[#73796F] hover:bg-[#F4F4EE] hover:text-[#252923] transition-colors cursor-pointer"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Regulatory Disclaimer Notice */}
            <div className="rounded-lg border border-[#F3E0B5] bg-[#FEF9EE] p-3 text-xs text-[#6A4700] flex items-start gap-2.5">
              <Info className="h-4 w-4 shrink-0 text-[#8A5C00] mt-0.5" />
              <div className="space-y-0.5">
                <span className="font-semibold text-[#8A5C00]">Monograph Reference Note: </span>
                <span>{selectedItem.note || 'Absence of a recorded warning does not imply universal safety. Reference data represents documented clinical findings.'}</span>
              </div>
            </div>

            {/* Description and Composition */}
            <div className="space-y-4 text-xs">
              {selectedItem.description && (
                <div>
                  <h4 className="font-bold text-[#252923] uppercase tracking-wider text-[11px] mb-1">
                    Description &amp; Intended Purpose
                  </h4>
                  <p className="leading-relaxed text-[#5E645A]">
                    {selectedItem.description}
                  </p>
                </div>
              )}

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                {selectedItem.active_ingredients && (
                  <div className="p-3 rounded-lg bg-[#FAF9F5] border border-[#E5E5DD]">
                    <span className="font-semibold text-[#252923] text-[11px] uppercase tracking-wider block mb-1">
                      Active Ingredients
                    </span>
                    <span className="text-[#5E645A] leading-relaxed block">
                      {selectedItem.active_ingredients}
                    </span>
                  </div>
                )}

                {selectedItem.ingredient_forms && (
                  <div className="p-3 rounded-lg bg-[#FAF9F5] border border-[#E5E5DD]">
                    <span className="font-semibold text-[#252923] text-[11px] uppercase tracking-wider block mb-1">
                      Commercial Forms &amp; Delivery
                    </span>
                    <span className="text-[#5E645A] leading-relaxed block">
                      {selectedItem.ingredient_forms}
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Dietary Compatibility Section */}
            <div className="space-y-2 pt-2 border-t border-[#E5E5DD]">
              <h4 className="font-bold text-[#252923] uppercase tracking-wider text-[11px]">
                Dietary Compatibility Attributes
              </h4>
              {selectedItem.diet_compat && selectedItem.diet_compat.length > 0 ? (
                <div className="divide-y divide-[#E5E5DD] rounded-lg border border-[#E5E5DD] overflow-hidden text-xs">
                  {selectedItem.diet_compat.map((dc, i) => (
                    <div key={`${dc.diet_code}-${i}`} className="p-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 bg-white">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-[#252923] capitalize">
                            {dc.diet_code}
                          </span>
                          <span
                            className={`px-1.5 py-0.5 rounded text-[10px] font-semibold uppercase ${
                              dc.compat_status === 'compatible'
                                ? 'bg-[#F0F7F3] text-[#235E3F] border border-[#CBE3D4]'
                                : 'bg-[#FEF9EE] text-[#8A5C00] border border-[#F3E0B5]'
                            }`}
                          >
                            {dc.compat_status}
                          </span>
                        </div>
                        {dc.notes && (
                          <p className="text-[11px] text-[#73796F] mt-1 leading-relaxed">
                            {dc.notes}
                          </p>
                        )}
                      </div>
                      {dc.source_ref && (
                        <span className="text-[10px] text-[#8E9589] shrink-0 sm:text-right">
                          Ref: {dc.source_ref}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-3 rounded-lg bg-[#FAF9F5] border border-[#E5E5DD] text-xs text-[#73796F]">
                  No specific dietary certifications recorded. Suitability depends on capsule material and excipients.
                </div>
              )}
            </div>

            {/* Allergen Warnings Section */}
            {selectedItem.allergens && selectedItem.allergens.length > 0 && (
              <div className="space-y-2 pt-2 border-t border-[#E5E5DD]">
                <h4 className="font-bold text-[#252923] uppercase tracking-wider text-[11px]">
                  Allergen Disclosures ({selectedItem.allergens.length})
                </h4>
                <div className="divide-y divide-[#E5E5DD] rounded-lg border border-[#E5E5DD] overflow-hidden text-xs">
                  {selectedItem.allergens.map((alg, i) => (
                    <div key={`${alg.allergen_code}-${i}`} className="p-3 flex items-start justify-between gap-2 bg-[#FFFDF9]">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-[#252923] capitalize">{alg.allergen_code}</span>
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-[#FEF9EE] text-[#8A5C00] border border-[#F3E0B5]">
                            {alg.relation?.replaceAll('_', ' ') || 'Notice'}
                          </span>
                        </div>
                        {alg.notes && (
                          <p className="text-[11px] text-[#73796F] mt-1">{alg.notes}</p>
                        )}
                      </div>
                      {alg.source_ref && (
                        <span className="text-[10px] text-[#8E9589] shrink-0">
                          {alg.source_ref}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Safety & Contraindication Rules Section */}
            <div className="space-y-2 pt-2 border-t border-[#E5E5DD]">
              <div className="flex items-center justify-between">
                <h4 className="font-bold text-[#252923] uppercase tracking-wider text-[11px]">
                  Configured Safety &amp; Interaction Rules ({selectedItem.safety_rules?.length || 0})
                </h4>
              </div>
              {selectedItem.safety_rules && selectedItem.safety_rules.length > 0 ? (
                <div className="divide-y divide-[#E5E5DD] rounded-lg border border-[#E5E5DD] overflow-hidden text-xs">
                  {selectedItem.safety_rules.map((sr) => {
                    const isExclusion = sr.action === 'exclude';
                    return (
                      <div key={sr.rule_id} className="p-3 space-y-1.5 bg-white">
                        <div className="flex items-center justify-between gap-2">
                          <span className="font-mono font-medium text-[11px] text-[#5E645A]">
                            {sr.rule_id} &middot; {sr.rule_type} ({sr.condition_code})
                          </span>
                          <span
                            className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                              isExclusion
                                ? 'bg-[#FDF2F2] text-[#9E2A2B] border border-[#F5C8C8]'
                                : 'bg-[#FEF9EE] text-[#8A5C00] border border-[#F3E0B5]'
                            }`}
                          >
                            {isExclusion ? 'Exclude' : 'Caution / Review'}
                          </span>
                        </div>
                        <p className="text-xs text-[#252923] leading-relaxed">
                          {sr.safety_message}
                        </p>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="p-3 rounded-lg bg-[#FAF9F5] border border-[#E5E5DD] text-xs text-[#73796F]">
                  No specific contraindication rules currently configured in this monograph. Note: The absence of a recorded warning does not imply safety for unrecorded health conditions or medications.
                </div>
              )}
            </div>

            {/* Goal Mappings Section */}
            <div className="space-y-2 pt-2 border-t border-[#E5E5DD]">
              <h4 className="font-bold text-[#252923] uppercase tracking-wider text-[11px]">
                Goal Scoring Mappings ({selectedItem.goal_mappings?.length || 0})
              </h4>
              {selectedItem.goal_mappings && selectedItem.goal_mappings.length > 0 ? (
                <div className="divide-y divide-[#E5E5DD] rounded-lg border border-[#E5E5DD] overflow-hidden text-xs">
                  {selectedItem.goal_mappings.map((gm) => (
                    <div key={gm.mapping_id} className="p-3 flex items-start justify-between gap-3 bg-white">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-[#252923] capitalize">
                            Goal: {gm.goal_id.replaceAll('_', ' ')}
                          </span>
                          <span className="text-[11px] text-[#73796F]">
                            ({gm.match_type} match)
                          </span>
                        </div>
                        {gm.evidence_notes && (
                          <p className="text-[11px] text-[#73796F] mt-1 leading-relaxed">
                            {gm.evidence_notes}
                          </p>
                        )}
                      </div>
                      <span className="font-mono text-xs font-bold text-[#244B38] bg-[#F0F7F3] border border-[#CBE3D4] px-2 py-0.5 rounded shrink-0">
                        +{gm.match_score} pts
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-3 rounded-lg bg-[#FAF9F5] border border-[#E5E5DD] text-xs text-[#73796F]">
                  No primary goal mappings configured for this supplement.
                </div>
              )}
            </div>

            {/* Source Reference & Footer */}
            <div className="pt-3 border-t border-[#E5E5DD] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-[#73796F]">
              <span>Primary Source: NIH Office of Dietary Supplements (ODS)</span>
              {selectedItem.source_url ? (
                <a
                  href={selectedItem.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 font-semibold text-[#244B38] hover:text-[#183627] hover:underline"
                >
                  <span>Open Professional Fact Sheet</span>
                  <ExternalLink className="h-3.5 w-3.5" />
                </a>
              ) : (
                <span className="text-[#8E9589]">No external fact sheet URL linked</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Standard Regulatory Disclaimer */}
      <MedicalDisclaimer compact />
    </div>
  );
};
